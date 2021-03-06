"""
Django settings for blog project.

Generated by 'django-admin startproject' using Django 4.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-t*^3rr6-2*r9w@(y2u$pq#*&1l#y+alvfd-u^*4m@+ql6^+3u_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app01.apps.App01Config',
    'api.apps.ApiConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'app01.middleware_custom.middleware_decode.Md1',
    'app01.middleware_custom.middleware_decode.Statistical',
]

ROOT_URLCONF = 'blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'blog.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blog',  # 数据库名
        'USER': 'blog',  # 用户名
        'PASSWORD': '123456',  # 密码
        'HOST': '127.0.0.1',  # 地址
        'PORT': '3306'  # 端口
    }
}

# 缓存配置
CACHES = {
    'default': {
        # 指定缓存使用的引擎
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        # 写在内存中的变量的唯一值
        'LOCATION': 'unique-snowflake',
        # 缓存超时时间(默认为300秒,None表示永不过期)
        'TIMEOUT': 300,
        'OPTIONS': {
            # 最大缓存记录的数量（默认300）
            'MAX_ENTRIES': 300,
            # 缓存到达最大个数之后，剔除缓存个数的比例，即：1/n（默认3）
            'CULL_FREQUENCY': 2,
        }
    }
}

# 用户扩展表设置
AUTH_USER_MODEL = 'app01.UserInfo'

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

# 重写了auth方法
AUTHENTICATION_BACKENDS = {
    'app01.valid.auth.CustomBackend',
}

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

# LANGUAGE_CODE = 'en-us'
#
# TIME_ZONE = 'UTC'

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/shanghai'

USE_I18N = True

# USE_TZ = True
USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
# 用户自己上传的文件
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 收集静态文件
STATIC_ROOT = os.path.join(BASE_DIR, 'rove_static')

# base64上传文件大小的限制
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5M

# simpleUI
SIMPLEUI_HOME_INFO = False  # 关闭服务器信息
# SIMPLEUI_HOME_QUICK = False  # 关闭快捷操作
# SIMPLEUI_HOME_ACTION = False  # 关闭最近动作

SIMPLEUI_HOME_PAGE = '/admin_home/'
SIMPLEUI_HOME_title = '首页'
SIMPLEUI_HOME_ICON = 'fa fa-user'

# 发送邮件

# 配置发送邮件的信息 
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.xxx.com'
EMAIL_PORT = 25
# 发送邮件的邮箱
EMAIL_HOST_USER = 'xxx@xx.com'
# 在邮箱中设置的客户端授权密码
EMAIL_HOST_PASSWORD = 'xxxx'
# 收件人看到的发件人
EMAIL_FROM = 'xxxxxx<xxxxxx@xxx.com>'

# 七牛云配置
QINIU_ACCESS_KEY = 'xxxxxx'
QINIU_SECRET_KEY = 'xxxxxx'
QINIU_BUCKET_NAME = 'xxxxxx-xxxxxx'
QINIU_SERVER_ADDR = 'http://xxxxxx.xxxxxx-xxxxxx.clouddn.com/'
