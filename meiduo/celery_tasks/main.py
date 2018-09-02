
#celery启动的入口"创建celery 对象,加载celery配置,注册celery
from celery import Celery

celery_app=Celery('celery_meiduo')

#加载celery
celery_app.config_from_object('celery_tasks.config')

#注册celery任务
celery_app.autodiscover_tasks(['celery_tasks.sms'])