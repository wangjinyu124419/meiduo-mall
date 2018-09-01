import random,logging

from django.shortcuts import render
from django_redis import get_redis_connection
from rest_framework.response import Response
from rest_framework.views import APIView
# Create your views here.
from meiduo.apps.verifications import constants
from meiduo.libs.yuntongxun.sms import CCP
logger=logging.getLogger('django')

class SMScodeview(APIView):
    def get(self,request,mobile):
        #生成短信验证码
        sms_code='%06d'%random.randint(0,999999)
        logger.info(sms_code)#直接用logging呢?
        #保存短信验证码导Redis
        myredis=get_redis_connection('verify_code')
        myredis.setex('sms_%s'%mobile,constants.SMS_CODE_REDIS_EXPIRES,sms_code)
        #使用容联发短信
        CCP().send_template_sms(mobile,[sms_code, constants.SMS_CODE_REDIS_EXPIRES//60],1)
        return  Response({'message':'ok'})