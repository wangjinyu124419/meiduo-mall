import re

from django.contrib.auth.backends import ModelBackend

from .models import User
# from users.models import User
# from meiduo.apps.users.models import User

def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    """
    return {
        'token': token,
        'user_id': user.id,
        'username': user.username
    }


# def jwt_response_payload_handler(token, user=None, request=None):
#     """
#     ⾃定义jwt认证成功返回数据
#     """
#     return {
#         'token': token,
#         'user_id': user.id,
#         'username': user.username,
#     }
def get_user_by_account(account):
    try:
        if re.match(r'^1[3-9]\d{9}$',account):
            user=User.objects.get(mobile=account)
        else:
            user=User.objects.get(username=account)
    except User.DoseNotExists:
        return None
    else:
        return user


#重写ModelBackend类
class UsernameMobileAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user=get_user_by_account(username)
        if user and user.check_password(password):
            return user
