from rest_framework import  serializers
from goods.models import SKU


class CartSelectAllSerializer(serializers.Serializer):
    """
    购物车全选
    """
    selected = serializers.BooleanField(label='全选')

class CartDeleteSerializer(serializers.Serializer):
    sku_id=serializers.IntegerField(label='商品id',min_value=1)
    def validate_sku_id(self,value):
        try:
            sku=SKU.objects.get(id=value)
        except SKU.DoesNotExist:
            raise  serializers.ValidationError('sku_id不存在')
        return value





class CartSKUSerializer(serializers.ModelSerializer):
    count=serializers.IntegerField(label='商品数量',min_value=1)
    selected=serializers.BooleanField(label='是否勾选',default=True)
    class Meta:
        model = SKU
        fields = ('id', 'count', 'name', 'default_image_url', 'price', 'selected')


class CartSerializer(serializers.Serializer):
    sku_id=serializers.IntegerField(label='商品ID',min_value=1)
    count=serializers.IntegerField(label='商品数量',min_value=1)
    selected=serializers.BooleanField(label='是否勾选',default=True)
    def validate_sku_id(self, value):
        #校验sku_id是否存在
        try:
            sku=SKU.objects.get(id=value)
        except SKU.DoesNotExist:
            raise  serializers.ValidationError('sku_id不存在')
        return value


