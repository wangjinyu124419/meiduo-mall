
#celery启动的入口"创建celery 对象,加载celery配置,注册celery
from celery import Celery

# 为celery使用django配置文件进行设置
import os
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'meiduo.settings.dev'

celery_app=Celery('celery_meiduo')

#加载celery
celery_app.config_from_object('celery_tasks.config')

#注册celery任务
celery_app.autodiscover_tasks(['celery_tasks.sms','celery_tasks.email'])