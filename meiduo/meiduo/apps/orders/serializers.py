from _decimal import Decimal

from django_redis import get_redis_connection
from django.utils import timezone
from rest_framework import serializers

from goods.models import SKU
from orders.models import OrderInfo, OrderGoods
from orders import models
from django.db import  transaction


class SaveOrderSerializer(serializers.ModelSerializer):
    """
    下单数据序列化器
    """
    class Meta:
        model = OrderInfo
        fields = ('order_id', 'address', 'pay_method')
        read_only_fields = ('order_id',)
        extra_kwargs = {
            'address': {
                'write_only': True,
                'required': True,
            },
            'pay_method': {
                'write_only': True,
                'required': True
            }
        }

    def create(self, validated_data):
        #重写create,实现订单表,订单商品表,sku,spu信息表的储存,不重新写只能保存OrderInfo
        """保存订单"""
        # 获取当前保存订单时需要的信息

        # order_id=时间+user_id
        user=self.context['request'].user
        order_id=timezone.now().strftime('%Y%m%d%H%M%S')+'%09d'%user.id
        address=validated_data.get('address')
        pay_method=validated_data.get('pay_method')
        # 保存订单基本信息 OrderInfo（⼀一）
        #明显的开启事物
        with transaction.atomic():
            save_id=transaction.savepoint()
            try:
                order=OrderInfo.objects.create(
                    order_id=order_id,
                    user = user,
                    address =address,
                    total_count = 0,
                    total_amount =Decimal('0.0'),
                    freight = Decimal('10.00'),
                    pay_method=pay_method,
                    status =OrderInfo.ORDER_STATUS_ENUM['UNPAID'] if  OrderInfo.PAY_METHODS_ENUM['CASH'] else OrderInfo.ORDER_STATUS_ENUM['UNPAID']
                )
                # 从redis读取购物⻋车中被勾选的商品信息
                redis_conn=get_redis_connection('cart')
                redis_seleceted=redis_conn.smembers('selected_%s'%user.id)
                redis_cart=redis_conn.hgetall('cart_%s'%user.id)

                #构造被勾选的商品字典

                # 遍历购物⻋车中被勾选的商品信息
                cart={}
                for sku_id in redis_seleceted:

                    cart[int(sku_id)]=int(redis_cart[sku_id])


                # 获取sku对象
                skus=SKU.objects.filter(id__in=cart.keys())
                # skus=SKU.objects.filter(id__in=cart.keys())

                # 判断库存
                for sku in skus:
                    while True:
                        sku_count = cart[sku.id]
                        orgin_stock=sku.stock
                        orgin_sale=sku.sales
                        if orgin_stock < sku_count :
                            transaction.savepoint_rollback(save_id)
                            raise serializers.ValidationError('库存不足')
                        import time
                        # time.sleep(5)
                    # 减少库存，增加销量量 SKU
                        #使用乐观锁并发下单,修改库存和销量
                        new_stock=orgin_stock-sku_count
                        new_sales=orgin_sale+sku_count
                        # ret = SKU.objects.filter(id=sku.id, stock=origin_stock).update(stock=new_stock, sales=new_sales)
                        # sku.stock=new_stock
                        # sku.sales=new_sales
                        # sku.save()
                        # sku_id=sku.id
                        # print(sku_id)
                        result=SKU.objects.filter(id=sku.id,stock=orgin_stock).update(stock=new_stock,sales=new_sales)
                        print(sku.stock)
                        if result == 0:
                            continue
                        # time.sleep(3)




                    # 修改SPU销量量
                        sku.goods.sales+=sku_count
                        sku.goods.save()


                    # 保存订单商品信息 OrderGoods（多）
                        OrderGoods.objects.create(
                            order=order,
                            sku=sku,
                            count = sku_count,
                            price = sku.price
                        )


                    # 累加计算总数量量和总价
                        order.total_count+=sku_count
                        order.total_amount+=sku_count*sku.price
                        break


                # 最后加⼊入邮费和保存订单信息or
                order.total_amount+=order.freight
                order.save()
            except serializers.ValidationError:
                raise
            except Exception:
                transaction.savepoint_rollback(save_id)
                raise
        transaction.savepoint_commit(save_id)
        print('new',sku.stock)

        # 清除购物⻋车中已结算的商品
        pl=redis_conn.pipeline()
        pl.hdel('cart_%s'%user.id,*redis_seleceted)
        pl.srem('selected_%s'%user.id,*redis_seleceted)
        pl.execute()

        return order
class CartSKUSerializer(serializers.ModelSerializer):
    """
    购物车商品数据序列
    """
    count = serializers.IntegerField(label='数量')

    class Meta:
        model = SKU
        fields = ('id', 'name', 'default_image_url', 'price', 'count')


class OrderSettlementSerializer(serializers.Serializer):
    """
    订单结算数据序列化器
    """
    freight = serializers.DecimalField(label='运费', max_digits=10, decimal_places=2)
    skus = CartSKUSerializer(many=True)