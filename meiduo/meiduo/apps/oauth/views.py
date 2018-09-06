from django.shortcuts import render
from QQLoginTool.QQtool import OAuthQQ
# Create your views here.
from rest_framework import status
from rest_framework.response import Response

from django.conf import settings
from rest_framework_jwt.settings import api_settings
from rest_framework.views import APIView
import  logging
from rest_framework.generics import GenericAPIView
# from itsdangerous import  TimedJSONWebSignatureSerializer as TJSSerializer
from .serializer import QQAuthUserSerializer
from .models import OAuthQQUser
from .utils import generate_save_user_token

logger=logging.getLogger('django')


from rest_framework.permissions import IsAuthenticated




#qq扫码后的登录回调
class QQAuthUserView(GenericAPIView):
    serializer_class = QQAuthUserSerializer
    def get(self,request):
        # 提取code请求参数
        code=request.query_params.get('code')
        if not code:
            return Response({'message':'缺少code'},status=status.HTTP_400_BAD_REQUEST)

        try:
            oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID, client_secret=settings.QQ_CLIENT_SECRET,
                                redirect_uri=settings.QQ_REDIRECT_URI)

        # 使⽤用code向QQ服务器器请求access_token
            access_token=oauth.get_access_token(code)

        # 使⽤用access_token向QQ服务器器请求openid
            open_id=oauth.get_open_id(access_token)
        except Exception as e:
            logging.info(e)
            return Response({'message':'qq服务器异常'},status=status.HTTP_503_SERVICE_UNAVAILABLE)

        # 使⽤用openid查询该QQ⽤用户是否在美多商城中绑定过⽤用户
        try:
            openid_user=OAuthQQUser.objects.get(openid=open_id)
        except OAuthQQUser.DoesNotExist:
        # 如果openid没绑定美多商城⽤用户，创建⽤用户并绑定到openid

            #不能铭文返回openid需要加密混淆
            openid_access_token=generate_save_user_token(open_id)
            return Response({'access_token':openid_access_token})

        else:
            # 如果openid已绑定美多商城⽤用户，直接⽣生成JWT token，并返回
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            # 获取oauth_user关联的user
            user = openid_user.user
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            return Response({
                'token': token,
                'user_id': user.id,
                'username': user.username
            })
        # 如果openid已绑定美多商城⽤用户，直接⽣生成JWT token，并返回
    def post(self,requset):
        serializer=self.get_serializer(data=requset.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)


        return Response({
            'token':token,
            'user_id':user.id,
            'username':user.username,

        })


class QQAuthURLView(GenericAPIView):
    def get(self,request):
        # url='https://graph.qq.com/oauth2.0/authorize'
        # params=# QQ登录参数
        # QQ_CLIENT_ID = '101474184'
        # QQ_CLIENT_SECRET = 'c6ce949e04e12ecc909ae6a8b09b637c'
        # QQ_REDIRECT_URI = 'http://www.meiduo.site:8080/oauth_callback.html''response_type=xx&client_id=xx&redirect_uri=xx&state=xx'
        # login_url=url+params
        # return Response({'login_url':login_url})

        #获取next参数
        # next=request.params_query.get('next')
        next = request.query_params.get('next')
        if not next:
            next='/'
        #创建OAuthQQ对象
        oauth=OAuthQQ(client_id=settings.QQ_CLIENT_ID,client_secret=settings.QQ_CLIENT_SECRET,redirect_uri=settings.QQ_REDIRECT_URI ,state=next)
        #调用扫码链接的方法
        login_url=oauth.get_qq_url()
        return Response({'login_url':login_url})

