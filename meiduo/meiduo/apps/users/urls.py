from django.conf.urls import url
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

from . import views
# from meiduo.apps.users import views

urlpatterns = [
    # 判断用户名是否重复
    url(r'^usernames/(?P<username>\w{5,20})/count/$', views.UsernameCountView.as_view()),
    # 判断手机号是否重复
    url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),
    # 注册
    url(r'^users/$', views.UserView.as_view()),
    # JWT登录
    url(r'^authorizations/$', obtain_jwt_token),
    # 用户基本信息
    url(r'^user/$', views.UserDetailView.as_view()),
    # 添加邮箱
    url(r'^email/$', views.EmailView.as_view()),
    #验证邮箱
    url(r'^emails/verificaion/$', views.VerifyEmailView.as_view()),
    url(r'^emails/verification/$', views.VerifyEmailView.as_view()),
]

router = routers.DefaultRouter()
router.register(r'addresses', views.AddressViewSet, base_name='addresses')

urlpatterns += router.urls