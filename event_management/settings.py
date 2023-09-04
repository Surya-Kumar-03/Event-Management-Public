"""
Django settings for event_management project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
from datetime import timedelta
from decouple import config as conf
import os


def empty_fun(val):
    return val


def config(key, cast=empty_fun, default=None):

    envfile = conf(key, cast=cast, default=default)
    if envfile:
        return envfile

    value = os.getenv(key)
    if value is None:
        return default
    else:
        if callable(cast):
            return cast(value)
        else:
            value
    return default


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-7!7*qbl(#kv!#e6!7n=&(56a-5wa2k!v-nz=f)5ush0+f4)b=='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool, default=True)
SESSION_EXP_TIME = config('SESSION_EXP_TIME', cast=eval,
                          default="1 * 24 * 60 * 60")

ALLOWED_HOSTS = ["*"]
INTERNAL_IPS = ['127.0.0.1']
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://localhost:3000",
    "http://192.168.67.144:3000"
]
CORS_URLS_REGEX = r"^/api/.*"

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    'user',
    'debug_toolbar',
    'django_extensions',
    'event',
    'mail',
    'django_cleanup.apps.CleanupConfig',
    'adminpanel'

]

SHELL_PLUS_PRE_IMPORTS = [('event_management.query_count', '*')]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'event_management.urls'
AUTH_USER_MODEL = 'user.User'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'event_management.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

if config('MYSQL_DATABASE', cast=bool, default=False):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': config("MYSQL_DATABASE_NAME"),
            'USER': config("MYSQL_DATABASE_USER"),
            'PASSWORD': config("MYSQL_DATABASE_PASSWORD"),
            'HOST': config('MYSQL_DATABASE_HOST'),
            'PORT': config('MYSQL_DATABASE_PORT', cast=int),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django rest framework
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated"
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        "rest_framework.authentication.SessionAuthentication",

    ),
    "DEFAULT_PAGINATION_CLASS": "event_management.pagination.CustomPagination",
    "PAGE_SIZE": 12,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ]
}

SIMPLE_JWT = {
    "TOKEN_OBTAIN_SERIALIZER": "event_management.serializers.TokenObtain",
    "ACCESS_TOKEN_LIFETIME": timedelta(seconds=config('ACCESS_TOKEN_EXP_TIME', cast=int)),
    "REFRESH_TOKEN_LIFETIME": timedelta(seconds=config('REFRESH_TOKEN_EXP_TIME', cast=int)),
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": config('JWT_SECRET_KEY', default=SECRET_KEY),
    "VERIFYING_KEY": "",
    "LEEWAY": timedelta(seconds=10)
}

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_USE_TLS = config('EMAIL_USE_TLS')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

OTP_VALIDITY_DURATION = 5 * 60  # in seconds

GIT_BUG_REPORT_API_KEY = config('GIT_BUG_REPORT_API_KEY', cast=str)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',  # Set the desired logging level
            'class': 'logging.FileHandler',
            'filename': 'db_queries.log',  # Set the file path for logging
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['file'],
            'propagate': False,
        },
    },
}
