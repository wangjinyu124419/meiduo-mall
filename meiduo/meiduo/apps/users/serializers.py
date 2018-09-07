import re

from django_redis import get_redis_connection
from rest_framework import serializers

from celery_tasks.email.tasks import send_verify_email
from .models import User,Address
from rest_framework_jwt.settings import api_settings


class UserAddressSerializer(serializers.ModelSerializer):
    """
    用户地址序列化器
    """
    province = serializers.StringRelatedField(read_only=True)
    city = serializers.StringRelatedField(read_only=True)
    district = serializers.StringRelatedField(read_only=True)
    province_id = serializers.IntegerField(label='省ID', required=True)
    city_id = serializers.IntegerField(label='市ID', required=True)
    district_id = serializers.IntegerField(label='区ID', required=True)

    class Meta:
        model = Address
        exclude = ('user', 'is_deleted', 'create_time', 'update_time')

    def validate_mobile(self, value):
        """
        验证手机号
        """
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式错误')
        return value

    #重写create方法,追加地址外键的user储存
    def create(self, validated_data):
        """
        保存
        """
        validated_data['user'] = self.context['request'].user
        address=Address.objects.create(**validated_data)
        return address
        # return super().create(validated_data)



class EmailSerializer(serializers.ModelSerializer):
    """
    邮箱序列化器
    """
    class Meta:
        model = User
        fields = ('id', 'email')
        extra_kwargs = {
            'email': {
                'required': True
            }
        }
    #只对email字段进行存储,
    #后续还会发邮件, 需要更新数据之后,返回响应前发送邮件
    # 所以要update方法

    def update(self, instance, validated_data):
        instance.email = validated_data['email']
        instance.save()

        # 更新邮箱之后,响应之前,发送验证邮件
        verify_url=instance.generate_email_verify_url()
        send_verify_email.delay(instance.email,verify_url)
        return instance

class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详细信息序列化器
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'mobile', 'email', 'email_active')


class CreateSerializer(serializers.ModelSerializer):
    # 定义模型外部字段
    password2 = serializers.CharField(label='确认密码', write_only=True)
    sms_code = serializers.CharField(label='短信验证码', write_only=True)
    allow = serializers.CharField(label='同意协议', write_only=True)
    token = serializers.CharField(label='登录状态token', read_only=True)  # 增加token字段
    class Meta:
        model=User
        # 所有字段：'id', 'username', 'mobile', 'password', 'password2', 'sms_code', 'allow'
        # 模型内部字段：'id', 'username', 'mobile', 'password'
        # 模型以外字段：'password2', 'sms_code', 'allow'
        # 输入字段(write_only)：'username', 'mobile', 'password', 'password2', 'sms_code', 'allow'
        # 输出字段(read_only)：'id', 'username', 'mobile'
        fields=['id',  'username', 'mobile', 'password', 'password2', 'sms_code', 'allow','token']
        extra_kwargs = {
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            }
        }
    def validate_mobile(self, value):
        """验证手机号"""
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式错误')
        return value

    def validate_allow(self, value):
        """检验用户是否同意协议"""
        if value != 'true':
            raise serializers.ValidationError('请同意用户协议')
        return value

    def validate(self, data):
        # 判断两次密码
        if data['password'] != data['password2']:
            raise serializers.ValidationError('两次密码不一致')

        # 判断短信验证码
        redis_conn = get_redis_connection('verify_codes')
        mobile = data['mobile']
        real_sms_code = redis_conn.get('sms_%s' % mobile)
        if real_sms_code is None:
            raise serializers.ValidationError('无效的短信验证码')
        if data['sms_code'] != real_sms_code.decode():
            raise serializers.ValidationError('短信验证码错误')

        return data
    def create(self, validated_data):
        #重写序列化的create方法,有些字段不能存到user模型对象
        del validated_data['password2']
        del validated_data['sms_code']
        del validated_data['allow']
        user=User.objects.create(**validated_data)

        #调用django系统加密方法
        user.set_password(validated_data['password'])
        user.save()

        #必须在注册或者登陆之后,响应注册或者登陆结果之前,生成jwt_token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        #生成载荷,包含了user_id和username,email
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        #生成user的token字段
        user.token=token

        return user
