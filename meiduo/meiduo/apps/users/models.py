from django.db import models
from django.contrib.auth.models import AbstractUser
from itsdangerous import TimedJSONWebSignatureSerializer as TJSSerializer, BadData
from django.conf import settings
from . import  constants
# Create your models here.

class User(AbstractUser):
    mobile=models.CharField(max_length=11,unique=True,verbose_name='手机号')
    email_active = models.BooleanField(default=False, verbose_name='邮箱验证状态')
    class Meta:
        db_table='tb_users'
        verbose_name='用户'
        verbose_name_plural=verbose_name

    def generate_email_verify_url(self):
        serializer=TJSSerializer(settings.SECRET_KEY,expires_in=constants.VERIFY_EMAIL_TOKEN_EXPIRES)
        data={
            'user_id':self.id,
            'email':self.email,
        }
        token=serializer.dumps(data).decode()
        print(token)
        verify_url = 'http://www.meiduo.site:8080/success_verify_email.html?token=' + token
        return verify_url

    @staticmethod
    def check_email_verify_token(token):
        serializer=TJSSerializer(settings.SECRET_KEY,expires_in=constants.VERIFY_EMAIL_TOKEN_EXPIRES)
        try:
            data=serializer.loads(token)
        except BadData:
            return None
        else:
            user_id=data.get('user_id')
            email=data.get('email')
        try:
            user=User.objects.get(id=user_id,email=email)
            # user=User.objects.get(id=user_id,)
        except User.DoesNotExist:
            return None
        else:
            return user
