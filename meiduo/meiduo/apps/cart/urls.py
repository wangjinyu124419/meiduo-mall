from . import views
from django.conf.urls import url
urlpatterns=[
    #添加购物车
    url(r'^cart/$',views.CartView.as_view())

]