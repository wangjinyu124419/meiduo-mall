import random,logging

from django.shortcuts import render
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
# Create your views here.
from celery_tasks.sms.tasks import sms_send_code
from meiduo.apps.verifications import constants
from meiduo.libs.yuntongxun.sms import CCP
logger=logging.getLogger('django')

class SMScodeview(APIView):
    def get(self,request,mobile):
        myredis = get_redis_connection('verify_code')
        send_flag=myredis.get('send_flag_%s'%mobile)
        if send_flag:
            return Response({'message':'60秒重复发送'},status=status.HTTP_400_BAD_REQUEST)
        #生成短信验证码
        sms_code='%06d'%random.randint(0,999999)
        logger.info(sms_code)#直接用logging呢?
        #redis管道优化代码,减少redis访问次数
        pl=myredis.pipeline()
        #保存短信验证码导Redis
        pl.setex('sms_%s'%mobile,constants.SMS_CODE_REDIS_EXPIRES,sms_code)
        pl.setex('send_flag_%s'%mobile,constants.SMS_CODE_EXPIRES,1)
        pl.execute()
        # myredis.setex('sms_%s'%mobile,constants.SMS_CODE_REDIS_EXPIRES,sms_code)
        # myredis.setex('send_flag_%s'%mobile,constants.SMS_CODE_EXPIRES,1)

        #使用容联发短信
        # CCP().send_template_sms(mobile,[sms_code, constants.SMS_CODE_REDIS_EXPIRES//60],1)
        #delay调用异步任务
        sms_send_code.delay(mobile,sms_code)
        return  Response({'message':'ok'})