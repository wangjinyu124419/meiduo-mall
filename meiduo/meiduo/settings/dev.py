#开发环境配置
"""
Django settings for meiduo project.

Generated by 'django-admin startproject' using Django 1.11.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""
import datetime
import os
import  sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#/home/python/PycharmProjects/meiduo_mall/meiduo/meiduo
print('根目录',BASE_DIR)

#追加导包路径
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# sys.path.append(os.path.join(BASE_DIR,'apps'))
#['/home/python/PycharmProjects/meiduo_mall/meiduo', '/home/python/PycharmProjects/meiduo_mall', '/home/python/.virtualenvs/meiduo/lib/python35.zip', '/home/python/.virtualenvs/meiduo/lib/python3.5', '/home/python/.virtualenvs/meiduo/lib/python3.5/plat-x86_64-linux-gnu', '/home/python/.virtualenvs/meiduo/lib/python3.5/lib-dynload', '/usr/lib/python3.5', '/usr/lib/python3.5/plat-x86_64-linux-gnu', '/home/python/.virtualenvs/meiduo/lib/python3.5/site-packages', '/home/python/PycharmProjects/meiduo_mall/meiduo/meiduo/apps']
print(sys.path)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 't$8(a_p^z%q6+l2ks4ey(#g#^!_1wrg2%5t2szt!amd-yn@r3u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['127.0.0.1', 'localhost','www.meiduo.site','api.meiduo.site']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',



    'rest_framework', # DRF
    'corsheaders', # JS跨域请求问题

    # 'meiduo_mall.apps.users.apps.UsersConfig', # 用户模块
    'users.apps.UsersConfig', # 用户模块，由用户模型类限制的此种注册方式
    'verifications.apps.VerificationsConfig', # 验证模块
    'oauth.apps.OauthConfig',
]

MIDDLEWARE = [
    # 放在中间件最外层的原因：跨域的问题需要在请求一开始就得到解决，所以需要优先执行，而中间件在处理请求时自上而下
    'corsheaders.middleware.CorsMiddleware', # 最外层的中间件,
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'meiduo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'meiduo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
     'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',  # 数据库主机
        'PORT': 3306,  # 数据库端口
        'USER': 'meiduo',  # 数据库用户名
        'PASSWORD': '124419',  # 数据库用户密码
        'NAME': 'meiduodb'  # 数据库名字
    }
}

#配置redis
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "session": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "verify_codes": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }


}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session"

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

# LANGUAGE_CODE = 'en-us'
#
# TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 是否禁用已经存在的日志器
    'formatters': {  # 日志信息显示的格式
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {  # 对日志进行过滤
        'require_debug_true': {  # django在debug模式下才输出日志
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {  # 日志处理方法
        'console': {  # 向终端中输出日志
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {  # 向文件中输出日志
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(BASE_DIR), "logs/meiduo.log"),  # 日志文件的位置
            'maxBytes': 300 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose'
        },
    },
    'loggers': {  # 日志器
        'django': {  # 定义了一个名为django的日志器
            'handlers': ['console', 'file'],  # 可以同时向终端与文件中输出日志
            'propagate': True,  # 是否继续传递日志信息
            'level': 'INFO',  # 日志器接收的最低日志级别
        },
    }
}
REST_FRAMEWORK = {
    # 异常处理
    'EXCEPTION_HANDLER': 'meiduo.utils.exceptions.exception_handler',
    # 认证
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',  # JWT认证，在前面的认证方案优先
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

# JWT_AUTH = {
#     # WT的有效期
#     'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
#     # 为JWT登录视图补充返回值
#     'JWT_RESPONSE_PAYLOAD_HANDLER': 'users.utils.jwt_response_payload_handler',
#
# }

JWT_AUTH = {
'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),

#重新指定JWT_RESPONSE_PAYLOAD_HANDLER方法
'JWT_RESPONSE_PAYLOAD_HANDLER':'users.utils.jwt_response_payload_handler',
}

AUTHENTICATION_BACKENDS = [
    'users.utils.UsernameMobileAuthBackend',
]
#制定默认用户模型类,语法规则必须是'应用名.模型类'
AUTH_USER_MODEL='users.User'
# CORS
CORS_ORIGIN_WHITELIST = (
'127.0.0.1:8080',
'localhost:8080',
'www.meiduo.site:8080',
'api.meiduo.site:8000',
)
CORS_ALLOW_CREDENTIALS = True # 允许携带cookie


# QQ登录参数
QQ_CLIENT_ID = '101474184'
QQ_CLIENT_SECRET = 'c6ce949e04e12ecc909ae6a8b09b637c'
QQ_REDIRECT_URI = 'http://www.meiduo.site:8080/oauth_callback.html'



#发送邮件配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 25
#发送邮件的邮箱
EMAIL_HOST_USER = 'wangjinyu124419@163.com'
#在邮箱中设置的客户端授权密码
EMAIL_HOST_PASSWORD = 'wangjinyu124419'
#收件人看到的发件人
EMAIL_FROM = 'wangjinyu<wangjinyu124419@163.com>'