"""
Django settings for OSINT_System project.

Generated by 'django-admin startproject' using Django 2.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

from huey import RedisHuey
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'wk@z!^we^q_-l_j6h+l4xq%vweos9tc^(_w1j!wwi35ud2$g8*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


#ESS_IP = '58.65.160.148'
#UIS_IP = '192.168.18.27'
#FILE_SERVER = '58.65.160.148'
#AIS_IP = '58.65.160.148'
#MONGO_DB = '192.168.18.20'



ESS_IP = '192.168.18.19'
UIS_IP = '192.168.18.77'
FILE_SERVER = '192.168.18.33'
AIS_IP = '192.168.18.13'
MONGO_DB = '192.168.18.20'


# mongoDb setting variables for public access
# db='OSINT_System'
# host='192.168.18.20'
# port=27017
#user = ''
#password = ''


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'channels',
    'background_task',
    'django_eventstream',
    'huey.contrib.djhuey',
    'User_Accounts_Management_Unit.apps.UserAccountsManagementUnitConfig',
    'OSINT_System_Core.apps.OsintSystemCoreConfig',
    'Public_Data_Acquisition_Unit.apps.PublicDataAcquisitionUnitConfig',
    'Data_Processing_Unit.apps.DataProcessingUnitConfig',
    'System_Log_Management_Unit.apps.SystemLogManagementUnitConfig',
    'Target_Management_System.apps.TargetManagementSystemConfig',
    'Portfolio_Management_System.apps.PortfolioManagementSystemConfig',
    'Case_Management_System.apps.CaseManagementSystemConfig',
    'Keybase_Management_System.apps.KeybaseManagementSystemConfig',
    'Avatar_Management_Unit.apps.AvatarManagementUnitConfig',
    'Bi_Tools.apps.BiToolsConfig',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django_grip.GripMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'OSINT_System.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'Data_Processing_Unit.context_processors.ess_ip',
                'Data_Processing_Unit.context_processors.uis_ip',
            ],
           
        },
    },
]

WSGI_APPLICATION = 'OSINT_System.wsgi.application'
ASGI_APPLICATION = 'OSINT_System.routing.application'

CORS_ORIGIN_ALLOW_ALL = True

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': '/etc/mysql/OSINT_System.cnf',
        },
    }
}
"""


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


"""
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated', )
}

"""


REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    )
}


CORS_ALLOW_CREDENTIALS = True


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
        },
        'simple': {
            'format': '%(levelname)s %(message)s',
        },
    },
    'handlers': {

        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'debug.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}


#from redis import ConnectionPool

#pool = ConnectionPool(host='my.redis.host', port=6379, max_connections=20)
HUEY = RedisHuey('my-app')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/


STATIC_SERVER_BASE_PATH = 'http://{0}/osint_system'.format(FILE_SERVER)
if(DEBUG):
    STATIC_URL = '/static/'
    STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"), )
else:
    STATIC_URL = STATIC_SERVER_BASE_PATH+'/static_files/'
    STATICFILES_DIRS = (os.path.join(STATIC_SERVER_BASE_PATH, "static_files"),)

STATIC_ROOT = os.path.join(BASE_DIR, "static_files")



MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/media/admin/'

"""

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = (os.path.join(BASE_DIR, "sfiles"), )



TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates'),)
TEMPLATE_LOADERS = (
'django.template.loaders.filesystem.Loader',
'django.template.loaders.app_directories.Loader',)

"""
