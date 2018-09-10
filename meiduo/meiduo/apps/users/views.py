from django.shortcuts import render

# Create your views here.
# url(r'^users/$', views.UserView.as_view()),
# url(r'^usernames/(?P<username>\w{5,20})/count/$', views.UsernameCountView.as_view()),
from rest_framework import status,mixins
from rest_framework.generics import CreateAPIView, RetrieveAPIView,UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from . import constants
from .models import User,Address
from . import serializers
from rest_framework.decorators import action


# url(r'^email/verificaion/$', views.VerifyEmailView.as_view()),

class AddressViewSet(mixins.CreateModelMixin,mixins.UpdateModelMixin,GenericViewSet):
    serializer_class = serializers.UserAddressSerializer
    permission_classes = [IsAuthenticated]
    def create(self,request,*args,**kwargs):
        #判断用户地址是否大188888888于上限20

        # count=requset.user.addresses.count()
        count=Address.objects.filter(user=request.user).count()
        if count>constants.USER_ADDRESS_COUNTS_LIMIT:
            return Response({'message':'超出上限'},status=status.HTTP_400_BAD_REQUEST)

        return super().create(request,*args,**kwargs)
        # serializer=self.get_serializer(data=requset.data)
        # serializer.is_valid(raise_exception=True)
        #
        #
        # serializer.save()
        #
        # #restful风格约束如果新增数据就要返回
        # return Response(serializer.data,status=status.HTTP_201_CREATED)
        #

    def get_queryset(self):
        return self.request.user.addresses.filter(is_deleted=False)
    queryset = Address.objects.all()
    def list(self, request, *args, **kwargs):
        """
        用户地址列表数据
        """
        # queryset = Address.objects.filter(user=request.user).all()
        # queryset = Address.objects.all()
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        user = self.request.user
        return Response({
            'user_id': user.id,
            'default_address_id': user.default_address_id,
            'limit': constants.USER_ADDRESS_COUNTS_LIMIT,
            'addresses': serializer.data,
        })
    # delete /addresses/<pk>/
    def destroy(self, request, *args, **kwargs):
        """
        处理删除
        """
        address = self.get_object()

        # 进行逻辑删除
        address.is_deleted = True
        address.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    # put /addresses/pk/status/
    @action(methods=['put'], detail=True)
    def status(self, request, pk=None):
        """
        设置默认地址
        """
        address = self.get_object()
        request.user.default_address = address
        request.user.save()
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)

    # put /addresses/pk/title/
    # 需要请求体参数 title
    @action(methods=['put'], detail=True)
    def title(self, request, pk=None):
        """
        修改标题
        """
        address = self.get_object()
        serializer = serializers.AddressTitleSerializer(instance=address, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

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