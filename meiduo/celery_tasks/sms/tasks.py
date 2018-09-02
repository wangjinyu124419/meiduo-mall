from .yuntongxun.sms import CCP
from . import constants

from celery_tasks.main import celery_app

#使用celery装饰其,将以下任务装饰为可以识别的异步任务
#name异步任务起别名
@celery_app.task(name='sms_send_code')
def sms_send_code(mobile,sms_code):

    CCP().send_template_sms(mobile,[sms_code, constants.SMS_CODE_REDIS_EXPIRES//60],1)
