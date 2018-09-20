from django.shortcuts import render
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.response import Response

from .serializers import ChannelSerializer, CategorySerializer
from .models import SKU, GoodsCategory
from . import serializers
# Create your views here.

from drf_haystack.viewsets import HaystackViewSet

class SKUSearchViewSet(HaystackViewSet):
    """
    SKU搜索f
    """
    index_models = [SKU]

    serializer_class = serializers.SKUIndexSerializer

# url(r'^categories/(?P<pk>\d+)/$', views.CategoryView.as_view()),
class CategoryView(GenericAPIView):
    """
    商品列表页面包屑导航
    """
    queryset = GoodsCategory.objects.all()

    def get(self, request, pk=None):
        ret = dict(
            cat1='',
            cat2='',
            cat3=''
        )
        category = self.get_object()
        if category.parent is None:
            # 当前类别为一级类别
            ret['cat1'] = ChannelSerializer(category.goodschannel_set.all()[0]).data
        elif category.goodscategory_set.count() == 0:
            # 当前类别为三级
            ret['cat3'] = CategorySerializer(category).data
            cat2 = category.parent
            ret['cat2'] = CategorySerializer(cat2).data
            ret['cat1'] = ChannelSerializer(cat2.parent.goodschannel_set.all()[0]).data
        else:
            # 当前类别为二级
            ret['cat2'] = CategorySerializer(category).data
            ret['cat1'] = ChannelSerializer(category.parent.goodschannel_set.all()[0]).data

        return Response(ret)

class SKUListView(ListAPIView):
    #指定序列化器
    serializer_class = serializers.SKUserializer

    #指定排序后端
    filter_backends = [OrderingFilter]

    #指定排序字段,由ordering接收
    ordering_fields = ('price', 'sales', 'create_time')

    #指定查询集
    # queryset = SKU.objects.all()
    def get_queryset(self):
        category_id=self.kwargs.get('category_id')
        # 由一模型类条件查询多模型类数据:
        # 语法如下
        # 一模型类关联属性名__一模型类属性名__条件运算符 = 值
        return SKU.objects.filter(category_id=category_id,is_launched=True)

