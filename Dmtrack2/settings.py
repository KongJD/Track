"""
Django settings for Dmtrack2 project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
import datetime

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'oej%bj2g*a*p$m49abea@x6l9sb$6t52cc!s99a7z&td!u2h+*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

CELERY_BROKER_URL = 'redis://127.0.0.1:6379/6' #配置代理人，指定代理人将任务存到哪里,这里是redis的1号库
CELERY_RESULT_BACKEND = 'django-db' #结果
BROKER_TRANSPORT = 'redis'
CELERY_TASK_SERIALIZER = 'json'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERYD_CONCURRENCY = 5 # 并发worker数
CELERYD_MAX_TASKS_PER_CHILD=60 ## 每个worker最多执行万60个任务就会被销毁，可防止内存泄露
CELERY_ACKS_LATE=True #允许重试
CELERYD_FORCE_EXECV=True #可以让Celery更加可靠,只有当worker执行完任务后,才会告诉MQ,消息被消费，防治死锁



# Application definition

INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_api_logger',
    'django_celery_results',
    'userapp',
    'backend',
]

#simpleui 配置
SIMPLEUI_STATIC_OFFLINE = True  # 打开simpleui离线模式
SIMPLEUI_HOME_INFO = False#服务器信息 隐藏
SIMPLEUI_ANALYSIS = False
SIMPLEUI_LOADING = False # 关闭Loading遮罩层
SIMPLEUI_LOGIN_PARTICLES= False#关闭登录页粒子动画效果
SIMPLEUI_STATIC_OFFLINE = True #离线模式

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'drf_api_logger.middleware.api_logger_middleware.APILoggerMiddleware', # Add here
]

ROOT_URLCONF = 'Dmtrack2.urls'

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

WSGI_APPLICATION = 'Dmtrack2.wsgi.application'


#修改DRF 认证
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",#API接口文档
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # 使用rest_framework_simplejwt(token)验证身份
        'rest_framework.authentication.SessionAuthentication',  # 基于用户名密码认证方式
        'rest_framework.authentication.BasicAuthentication'  # 基于Session认证方式
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'  # 默认权限为验证用户
    ],

}



SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=10),##token 有效时长，返回access有效时长
    'REFRESH_TOKEN_LIFETIME':datetime.timedelta(days=5),##token 刷新的有效时长，返回refresh的有效时长
    'UPDATE_LAST_LOGIN':True,
}

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'Dmtrackdb2',
        'USER': 'siteusrC',
        'PASSWORD': 'dm20220418!',
        'HOST':'192.168.100.10',
        'PORT':'3306',
        'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                'charset':'utf8',
                'isolation_level':None
        }

    }

}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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


DRF_API_LOGGER_DATABASE = True  # Default to False ,for drf-api-logger
# 日志配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
        "default": {
            "format": '%(asctime)s %(name)s  %(pathname)s:%(lineno)d %(module)s:%(funcName)s '
                      '%(levelname)s- %(message)s',
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        },
        'file': {
            'level': 'DEBUG',
            #'class': 'logging.handlers.TimedRotatingFileHandler',单进程下日志可以按照日期分割，多进程失效
            'class':'backend.MultiCompatibleHandler.MultiCompatibleTimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'log/django_logs/debug.log'),
            'when': "D",
            'interval': 1,
            'formatter': 'default',
            'encoding': 'utf-8'
        },
        "request": {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'log/django_logs/request.log'),
            'formatter': 'default'
        },
        "server": {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'log/django_logs/server.log'),
            'formatter': 'default'
        },
        "root": {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'log/django_logs/root.log'),
            'formatter': 'default'
        },
 
        "db_backends": {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'log/django_logs/db_backends.log'),
            'formatter': 'default'
        },
        "autoreload": {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'log/django_logs/autoreload.log'),
            'formatter': 'default'
        },
	"restful_api":{
            'level' :'DEBUG',
    	    'class': 'backend.MultiCompatibleHandler.MultiCompatibleTimedRotatingFileHandler',
	    'filename': os.path.join(BASE_DIR, 'log/django_logs/api.log'),
	    'formatter':'default',
	}

    },
    'loggers': {
        # 应用中自定义日志记录器
        'mylogger': {
            'level': 'DEBUG',
            'handlers': ['console', 'file'],
            'propagate': True,
        },
        "django": {
            "level": "DEBUG",
            "handlers": ["console", "file"],
            'propagate': False,
        },
        "django.request": {
            "level": "DEBUG",
            "handlers": ["request"],
            'propagate': False,
        },
        "django.server": {
            "level": "DEBUG",
            "handlers": ["server"],
            'propagate': False,
        },
        "django.db.backends": {
            "level": "DEBUG",
            "handlers": ["db_backends"],
            'propagate': False,
        },
        "django.utils.autoreload": {
            "level": "INFO",
            "handlers": ["autoreload"],
            'propagate': False,
        },
        "api":{
            "level": "INFO",
            "handlers":['restful_api'],
            "propagate": True
        }
    },
    'root': {
        "level": "DEBUG",
        "handlers": ["root"],
    }
}


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

#STATICFILES_DIRS = os.path.join(BASE_DIR, 'dist/static'),

STATIC_ROOT = os.path.join(BASE_DIR, 'static')


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# 将用户model指向已创建新的用户model
AUTH_USER_MODEL = 'userapp.NewUser'


#drf_api_logger 配置
DRF_API_LOGGER_DATABASE = True  # 存储到数据库
DRF_API_LOGGER_SIGNAL = True  # Listen to the signal as soon as any API is called. So you can log the API data into a file or for different use-cases.
DRF_LOGGER_QUEUE_MAX_SIZE = 50  # 多少条日志写入 Default to 50 if not specified.
DRF_LOGGER_INTERVAL = 10  # 间隔多久写入 In Seconds, Default to 10 seconds if not specified.
DRF_API_LOGGER_SKIP_NAMESPACE = []  # 指定app不写入
DRF_API_LOGGER_SKIP_URL_NAME = []  # 指定url不写入
DRF_API_LOGGER_DEFAULT_DATABASE = 'default'  # 指定数据库 如果未指定，默认为“default”确保迁移 DRF_API_LOGGER_DEFAULT_DATABASE 中指定的数据库。
DRF_API_LOGGER_PATH_TYPE = 'ABSOLUTE'  # 完整路径
DRF_API_LOGGER_SLOW_API_ABOVE = 200  # 额外标识超过200ms的请求 默认为无
DRF_API_LOGGER_EXCLUDE_KEYS  = [] # 敏感数据将被替换为“***FILTERED***”。