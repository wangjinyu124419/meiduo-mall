from django.shortcuts import render

# Create your views here.
# url(r'^users/$', views.UserView.as_view()),
# url(r'^usernames/(?P<username>\w{5,20})/count/$', views.UsernameCountView.as_view()),
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView,UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from . import serializers

# url(r'^email/verificaion/$', views.VerifyEmailView.as_view()),




class VerifyEmailView(APIView):
    def get(self,requset):
        token=requset.query_params.get('token')
        if not token:
            return Response({'message':'缺少token'},status=status.HTTP_400_BAD_REQUEST)
        #token中读取用户信息
        #用类调用实例方法
        user=User.check_email_verify_token(token)
        if not user:
            return Response({'message':'无效token'},status=status.HTTP_400_BAD_REQUEST)
        user.email_active=True
        user.save()
        return Response({'message':'Ok'})






class EmailView(UpdateAPIView):
    serializer_class = serializers.EmailSerializer
    permission_classes = [IsAuthenticated]
    #重写get方法
    def get_object(self):
        return self.request.user

# url(r'^users/$', views.UserView.as_view()),

class UserDetailView(RetrieveAPIView):
    """
    用户详情
    """
    serializer_class = serializers.UserDetailSerializer
    permission_classes = [IsAuthenticated]

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