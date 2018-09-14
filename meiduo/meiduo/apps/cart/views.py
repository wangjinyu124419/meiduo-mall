import base64

import pickle
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


from goods.models import SKU
from . import serializers
from django_redis import get_redis_connection

class CartSelectAllView(APIView):
    """
    购物车全选
    """
    def perform_authentication(self, request):
        """
        重写父类的用户验证方法，不在进入视图前就检查JWT
        """
        pass

    def put(self, request):
        serializer = serializers.CartSelectAllSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        selected = serializer.validated_data['selected']

        try:
            user = request.user
        except Exception:
            # 验证失败，用户未登录
            user = None

        #如果用户登陆
        if user and user.is_authenticated:


            redis_conn=get_redis_connection('cart')
            pl=redis_conn.pipeline()
            redis_cart_dict=redis_conn.hgetall('cart_%s'%user.id)
            sku_ids=redis_cart_dict.keys()
            if selected:
                redis_conn.sadd('selected_%s'%user.id,*sku_ids)
            else:
                redis_conn.srem('selected_%s'%user.id,*sku_ids)
            # pl.execute()
            return Response({'message','OK'})
        else:
            # cookie
            cart = request.COOKIES.get('cart')
            response = Response({'message': 'OK'})
            if cart is not None:
                cart = pickle.loads(base64.b64decode(cart.encode()))
            for sku_id in cart:
                cart[sku_id]['selected'] = selected
            cookie_cart = base64.b64encode(pickle.dumps(cart)).decode()
            # 设置购物⻋车的cookie
            # 需要设置有效期，否则是临时cookie
            response.set_cookie('cart', cookie_cart)
            return response


# Create your views here.
class CartView(APIView):
    #购物车增删改查

    def perform_authentication(self, request):
        #重写认证,直接pass,不对用户做认证,认证的行为方法具体需要的地方,自己决定.
        pass

    #添加购物车
    def post(self,request):
        serializer=serializers.CartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        sku_id=serializer.validated_data.get('sku_id')
        count=serializer.validated_data.get('count')
        selected=serializer.validated_data.get('selected')

        #判断用户是否登陆
        try:
            user = request.user

        except Exception:
            user = None
        # if request.user is not None and request.user.is_authenticated:
        if user and user.is_authenticated:

            redis_conn=get_redis_connection('cart')
            pl=redis_conn.pipeline()
            # redis_cart=redis_conn.hgetall()
            # hincrby(name, key, amount=1)
            #未哈希表key中的域field的值增量increment
            pl.hincrby('cart_%s'%user.id,sku_id,count)

            #储存值是否被勾选
            # 默认值是true,但是还要加下判断
            if selected:
                pl.sadd('selected_%s'%user.id,sku_id)
            pl.execute()
            return Response(serializer.data,status=status.HTTP_201_CREATED)

        else:
            #获取cookie数据
            cart_str=request.COOKIES.get('cart')
            if cart_str:
                cart_str_bytes=cart_str.encode()
                #将bytes的类型的字符串转成bytes类型的字典
                cart_dict_bytes=base64.b64decode(cart_str_bytes )
                print(type(cart_dict_bytes))

                #讲bytes类型的字典转成标准字典
                cart_dict=pickle.loads(cart_dict_bytes)
            else:
                cart_dict={}

            if sku_id in cart_dict:
                origin_count=cart_dict[sku_id]['count']
                count+=origin_count
            cart_dict[sku_id]={
                'count':count,
                'selected':selected,
            }


            #讲数据写入到cookie中
            cart_dict_bytes=pickle.dumps(cart_dict)
            cart_str_bytes=base64.b64encode(cart_dict_bytes)
            cart_str=cart_str_bytes.decode()

            respone=Response(serializer.data,status=status.HTTP_201_CREATED)
            respone.set_cookie('cart',cart_str)
            return respone

    def get(self,request):
        # 判断用户是否登陆
        print(request)
        try:
            user = request.user

        except Exception:
            user = None
            # if request.user is not None and request.user.is_authenticated:
        if user and user.is_authenticated:
            redis_conn=get_redis_connection('cart')
            redis_cart_dict=redis_conn.hgetall('cart_%s'%user.id)
            # redis_cart__dict={b'sku_id_1',b'count_1'}
            redis_selected=redis_conn.smembers('selected_%s'%user.id)
            # redis_selected=[b'sku_id']
            cart_dict={}
            for sku_id,count in redis_cart_dict.items():
                cart_dict[int(sku_id)]={
                    'count':int(count),
                    'selected':sku_id in redis_selected
                }

        else:
            cart_str = request.COOKIES.get('cart')
            if cart_str:
                cart_str_bytes = cart_str.encode()
                # 将bytes的类型的字符串转成bytes类型的字典
                cart_dict_bytes = base64.b64decode(cart_str_bytes)
                print(type(cart_dict_bytes))

                # 讲bytes类型的字典转成标准字典
                cart_dict = pickle.loads(cart_dict_bytes)
            else:
                cart_dict = {}

        sku_ids=cart_dict.keys()
        skus=SKU.objects.filter(id__in=sku_ids)
        for sku in skus:
            sku.count=cart_dict[sku.id]['count']
            sku.selected=cart_dict[sku.id]['selected']

        serializer=serializers.CartSKUSerializer(skus,many=True)
        return Response(serializer.data)

    def put(self,request):
        serializer = serializers.CartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        sku_id = serializer.validated_data.get('sku_id')
        count = serializer.validated_data.get('count')
        selected = serializer.validated_data.get('selected')

        # 判断用户是否登陆
        try:
            user = request.user

        except Exception:
            user = None
        # if request.user is not None and request.user.is_authenticated:
        if user and user.is_authenticated:

            redis_conn = get_redis_connection('cart')
            pl = redis_conn.pipeline()
            #直接覆盖以存在的购物车数据
            pl.hset('cart_%s'%user.id,sku_id,count)
            # 储存值是否被勾选
            # 默认值是true,但是还要加下判断
            if selected:
                pl.sadd('selected_%s' % user.id, sku_id)
            else:
                pl.srem('selected_%s' % user.id, sku_id)
            pl.execute()
            print('打印',serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            # 获取cookie数据
            cart_str = request.COOKIES.get('cart')
            if cart_str:
                cart_str_bytes = cart_str.encode()
                # 将bytes的类型的字符串转成bytes类型的字典
                cart_dict_bytes = base64.b64decode(cart_str_bytes)


                # 讲bytes类型的字典转成标准字典
                cart_dict = pickle.loads(cart_dict_bytes)
            else:
                cart_dict = {}

            cart_dict[sku_id] = {
                'count': count,
                'selected': selected,
            }

            # 讲数据写入到cookie中
            cart_dict_bytes = pickle.dumps(cart_dict)
            cart_str_bytes = base64.b64encode(cart_dict_bytes)
            cart_cookie_str = cart_str_bytes.decode()

            respone = Response(serializer.data,)
            respone.set_cookie('cart', cart_cookie_str)
            return respone


    def delete(self,request):
        #校验数据
        serializer=serializers.CartDeleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        #取出校验后的id
        sku_id=serializer.validated_data.get('sku_id')

        #判断用户是否登陆
        try:
            user=request.user
        except Exception:
            user=None
        if user and user.is_authenticated:

            #操作redis
            redis_conn = get_redis_connection('cart')
            pl = redis_conn.pipeline()
            pl.hdel('cart_%s'%user.id,sku_id)
            pl.srem('selected_%s'%user.id,sku_id)
            pl.execute()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            #操作cookie
            cart_str = request.COOKIES.get('cart')
            if cart_str:
                cart_str_bytes = cart_str.encode()
                # 将bytes的类型的字符串转成bytes类型的字典
                cart_dict_bytes = base64.b64decode(cart_str_bytes)

                # 讲bytes类型的字典转成标准字典
                cart_dict = pickle.loads(cart_dict_bytes)
            else:
                cart_dict={}
            respone = Response(status=status.HTTP_204_NO_CONTENT)

            if sku_id in cart_dict:
                del cart_dict[sku_id]
                # 讲数据写入到cookie中
                cart_dict_bytes = pickle.dumps(cart_dict)
                cart_str_bytes = base64.b64encode(cart_dict_bytes)
                cart_cookie_str = cart_str_bytes.decode()

                respone.set_cookie('cart', cart_cookie_str)

            return respone



