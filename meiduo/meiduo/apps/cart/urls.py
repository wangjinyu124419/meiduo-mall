from . import views
from django.conf.urls import url
urlpatterns=[
    #添加购物车
    url(r'^carts/$',views.CartView.as_view()),
    #购物车全选
    url(r'^carts/selection/$', views.CartSelectAllView.as_view()),

]