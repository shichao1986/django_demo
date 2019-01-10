"""
Django settings for DjangoDemoProj project.

Generated by 'django-admin startproject' using Django 1.11.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# django项目的根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'x12kp7non3*d#8fvq3s_$j^+n9@rbi%x)ilbb7v_w_h634dn=k'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

LOGIN_URL = '/admin/login/'

# Age of cookie, in seconds (default: 2 weeks). We set it to 1 day
SESSION_COOKIE_AGE = 60 * 60 * 24
# Whether a user's session cookie expires when the Web browser is closed.
# 浏览器关闭时session过期指的是在浏览器关闭时清除浏览器cookie中的的sessionid的值
# 服务端在浏览器关闭时并不会删除session
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'helloworld',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #CSRF token用于防止csrf攻击，需要前端在每一个post请求中增加csrfmiddlewaretoken字段，
    # put 和 delete时可在header头中增加HTTP_X_CSRFTOKEN（HTTP-X-CSRFTOKEN）
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'helloworld.middleware.UserLoginMiddleware',
]

ROOT_URLCONF = 'DjangoDemoProj.urls'

# 模板文件django会在每个app的目录下的templates文件夹下搜索，此处
# DIRS :[] 中增加的路径为公共模板的放置路径，此处的模板也会被django找到
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

WSGI_APPLICATION = 'DjangoDemoProj.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# django 自带的数据表存入default数据库，app相关数据表存入postgresql_db1
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'djangodemo-db',
        'USER': 'djangodemo-user',
        'PASSWORD': 'password',
        'HOST': '10.6.3.29',
        'PORT': '25432',
        'CONN_MAX_AGE': 600,
    },
    'postgresql_db1': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'djangodemo-db',
        'USER': 'djangodemo-user',
        'PASSWORD': 'password',
        'HOST': '10.6.3.29',
        'PORT': '25433',
        'CONN_MAX_AGE': 600,
    }
}

# # DATABASE_ROUTERS list 可以有多个，匹配的顺序按照list中的自然顺序从左向右
DATABASE_ROUTERS = ['DjangoDemoProj.db_router.AppsDbRouter']
#
# # app与其使用的db的映射关系
DATABASE_APPS_MAPPING = {
    'helloworld':'postgresql_db1',
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

# STATIC_ROOT 用于执行 python manage.py collectstatic， 会将各个app下的static文件全部拷贝到STATIC_ROOT指定的路径下
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATIC_URL
STATIC_URL = '/static/'

# STATICFILES_DIRS 为公共的static文件夹存放位置，其内部的路径也是django可以找到的，默认为空
# 执行 python manage.py collectstatic 时也会将STATICFILES_DIRS 拷贝到 STATIC_ROOT，所以
# STATICFILES_DIRS中不能包含STATIC_ROOT在内
STATICFILES_DIRS = [
]

# 这个是默认设置，Django 默认会在 STATICFILES_DIRS中的文件夹 和 各app下的static文件夹中找文件
# 注意有先后顺序，找到了就不再继续找了
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder"
)

# 配置django的日志
'''
disable_existing_loggers 为False 使用django默认的 loggers，此时
DEBUG = True
‘django’这个logger以及其（除了django.server之外的）所有下级的INFO以上的日志，都会被StreamHandler处理（输出到console）
DEBUG = Flase
‘django’这个logger以及其（除了django.server之外的）所有下级的ERROR和CRITICAL的日志，都会被AdminEmailHandler处理（发送至指定邮件）

如果
disable_existing_loggers 为True，则不适用django默认的loggers，此时需要重新定义
‘django’这个logger，对于未定义的logger会失去对应的日志
'''

# 使用django发送邮件日志时的邮件配置
# 将配置修改正确即可
EMAIL_HOST = 'smtp.xxxx.com'  # SMTP地址
EMAIL_PORT = 25  # SMTP端口
EMAIL_HOST_USER = 'yourname@xxxx.com'  # 发送邮件的邮箱
EMAIL_HOST_PASSWORD = '******'  # 我的邮箱密码
EMAIL_SUBJECT_PREFIX = '[这是主题前缀]'  # 为邮件Subject-line前缀,默认是'[django]'
EMAIL_USE_TLS = False  # 与SMTP服务器通信时，是否启动TLS链接(安全链接)。默认是false,根据邮件服务器的情况进行配置
# 管理员站点
DEFAULT_FROM_EMAIL = SERVER_EMAIL = EMAIL_HOST_USER  # The email address that error messages come from, such as those sent to ADMINS and MANAGERS.
ADMINS = (('admin', 'yourname@xxxx.com'),)  # 接收邮件的邮箱（或邮件组）,django 管理员用户


LOGGING = {
    'version' :1,
    # 使用默认的django loggers
    'disable_existing_loggers' : False,
    'formatters': {
        'standard':{
            'format':'%(asctime)s %(name)s %(levelname)s %(filename)s [%(funcName)s %(lineno)s]: %(message)s'
        }
    },
    'filters': {

    },
    'handlers': {
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter':'standard'
        },
        # 该handler 会将邮件发送给ADMINS中定义的管理员及其邮箱
        'email_handler':{
            'level':'ERROR',
            'class':'django.utils.log.AdminEmailHandler',
            'formatter':'standard'
        }
    },
    'loggers':{
        'log1':{
            'handlers':['console'],
            'level':'DEBUG',
            'propagate': True
        },
        # 'log2':{
        #     'handlers':['email_handler'],
        #     'level':'ERROR',
        #     'propagate':False
        # },
        'django.db.backends':{
            'handlers':['console'],
            'level':'DEBUG' if DEBUG else 'INFO'
        }
    }
}