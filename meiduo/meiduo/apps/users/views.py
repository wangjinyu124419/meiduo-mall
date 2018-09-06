from django.shortcuts import render

# Create your views here.
# url(r'^users/$', views.UserView.as_view()),
# url(r'^usernames/(?P<username>\w{5,20})/count/$', views.UsernameCountView.as_view()),
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from . import serializers


# url(r'^users/$', views.UserView.as_view()),

class UserDetailView(RetrieveAPIView):
    """
    用户详情
    """
    serializer_class = serializers.UserDetailSerializer
    # permission_classes = [IsAuthenticated]

    #重写get方法
    def get_object(self):
        return self.request.user

class UserView(CreateAPIView):
    """
    用户注册
    传入参数：
        username, password, password2, sms_code, mobile, allow
    """
    serializer_class = serializers.CreateSerializer

# url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),
class MobileCountView(APIView):
    def get(self,request,mobile):
        count = User.objects.filter(mobile=mobile).count()

        data = {
            'mobile': mobile,
            'count': count
        }
        return Response(data)

class UsernameCountView(APIView):
    def get(self,requset,username):
        count=User.objects.filter(username=username).count()

        data={
            'username':username,
            'count':count
        }
        return Response(data)