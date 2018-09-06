from itsdangerous import  TimedJSONWebSignatureSerializer as TJWSerializer, BadData
from django.conf import settings
def generate_save_user_token(openid):
    #使用dangerous模块进行签名
    serializer=TJWSerializer(settings.SECRET_KEY,600)
    print(settings.SECRET_KEY)

    data={'openid':openid}
    token=serializer.dumps(data)
    token=token.decode()
    return token

def check_save_user_token(access_token):

    serializer=TJWSerializer(settings.SECRET_KEY,600)
    try:
        data=serializer.loads(access_token)
    except BadData:
        return None
    else:
        openid=data.get('openid')
        return  openid

