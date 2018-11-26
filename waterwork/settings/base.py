"""
Django settings for leakage project.

Generated by 'django-admin startproject' using Django 1.11.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'v(&!is%xev5j)%kor)oy3ww^(ipa8rnk=)xbr^gg59nc5czi=8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

INTERNAL_IPS =['192.168.1.110']
# Celery settings

CELERY_BROKER_URL = 'amqp://guest:guest@localhost//'

#: Only add pickle to this list if your broker is secured
#: from unwanted access (see userguide/security.html)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_BACKEND = 'db+sqlite:///results.sqlite'
CELERY_TASK_SERIALIZER = 'json'


# BROKER_URL = 'amqp://guest:guest@localhost//'
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mptt',
    'import_export',
    'accounts',
    'legacy',
    
    'prodschedule',
    'monitor',
    'analysis',
    'alarm',
    'baseanalys',
    'gis',
    'entm',
    'devm',
    'dmam',
    'reports',
    'sysm',
    'wirelessm',
    # 'debug_toolbar',
    # 'channels',
    'django_apscheduler',
    'shexian',
]


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', # this is default
    # 'guardian.backends.ObjectPermissionBackend',
)


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'waterwork.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,"templates"),os.path.join(BASE_DIR,"echarts","map","province")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'waterwork.wsgi.application'

# IMPORT_EXPORT_USE_TRANSACTIONS = True

# ASGI_APPLICATION = "waterwork.routing.application"

# Database
# yum install mysql mysql-devel mysql-lib
# pip install mysqlclient
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'virvo_dev2.db'),
    # },
    # 'default': { 
    #     'ENGINE': 'django.contrib.gis.db.backends.postgis',#postgresql_psycopg2  or django.contrib.gis.db.backends.postgis or django.db.backends.postgresql_psycopg2
    #     'NAME': 'waterwork',
    #     'USER': 'scada',
    #     'PASSWORD': 'scada',
    #     'HOST': 'localhost',    #120.78.255.129 192.168.197.134
    #     'PORT': '5432',
    # },
    'default': {
        'ENGINE': 'django.db.backends.mysql',#postgresql_psycopg2  or django.contrib.gis.db.backends.postgis or django.db.backends.postgresql_psycopg2
        'NAME': 'waterwork',
        'USER': 'scada',
        'PASSWORD': 'scada',
        'HOST': '192.168.1.27',
        'PORT': '3306',
        'OPTIONS':{
            'init_command':"SET sql_mode='STRICT_TRANS_TABLES'",
            # 'charset':'utf8mb4',
        }
    },
    'zncb': {
        'ENGINE': 'django.db.backends.mysql',#postgresql_psycopg2  or django.contrib.gis.db.backends.postgis or django.db.backends.postgresql_psycopg2
        'NAME': 'zncb',
        'USER': 'scada',
        'PASSWORD': 'scada',
        'HOST': '192.168.1.27', #220.179.118.150-shexian 120.78.255.129-virvo  192.168.1.27
        'PORT': '3306',
        'OPTIONS':{
            'init_command':"SET sql_mode='STRICT_TRANS_TABLES'",
            # 'charset':'utf8mb4',
        }
    },
    # 'shexian': {
    #     'ENGINE': 'django.db.backends.mysql',#postgresql_psycopg2  or django.contrib.gis.db.backends.postgis or django.db.backends.postgresql_psycopg2
    #     'NAME': 'zncb',
    #     'USER': 'scada',
    #     'PASSWORD': 'scada',
    #     'HOST': '220.179.118.150', #220.179.118.150-shexian 120.78.255.129-virvo  192.168.1.27
    #     'PORT': '3306',
    #     'OPTIONS':{
    #         'init_command':"SET sql_mode='STRICT_TRANS_TABLES'",
    #         # 'charset':'utf8mb4',
    #     }
    # },
    # 'gis': { http://120.78.255.129
    #     'ENGINE': 'django.contrib.gis.db.backends.postgis',#postgresql_psycopg2  or django.contrib.gis.db.backends.postgis or django.db.backends.postgresql_psycopg2
    #     'NAME': 'scada',
    #     'USER': 'scada',
    #     'PASSWORD': 'scada',
    #     'HOST': 'localhost',
    #     'PORT': '5432',
    # },
}

DATABASE_ROUTERS = ['legacy.routers.LegacyRouter', ]

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

AUTH_USER_MODEL = 'accounts.User' #change buikld-in user model to us
# AUTH_GROUP_MODEL = 'accounts.MyRoles'

LOGIN_URL = '/login/'
LOGIN_URL_REDIRECT = '/'
LOGOUT_URL = '/logout/'

LOGOUT_REDIRECT_URL = '/login/'

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'    #'UTC'

USE_I18N = True

USE_L10N = False

USE_TZ = False

DATE_INPUT_FORMATS = ['%d-%m-%Y']

#add geospatial something
GEOS_LIBRARY_PATH = '/usr/local/lib/libgeos_c.so'
GDAL_LIBRARY_PATH = '/usr/local/lib/libgdal.so'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR,'static')
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "assets"),
    
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# MEDIA_ROOT = os.path.join(BASE_DIR, 'data/') # 'data' is my media folder
# MEDIA_URL = '/media/'

try:
    from .loggers_development import *
except Exception as e:
    pass