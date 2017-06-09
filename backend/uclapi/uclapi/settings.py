"""
Django settings for uclapi project.

Generated by 'django-admin startproject' using Django 1.10.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import requests
from distutils.util import strtobool

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
# This value should be set by the UCLAPI_PRODUCTION environment variable anyway.
# If in production, debug should be false
DEBUG = not strtobool(os.environ.get("UCLAPI_PRODUCTION", "False"))

ALLOWED_HOSTS = ["localhost"]

# If a domain is specified then make this an allowed host
if os.environ.get("UCLAPI_DOMAIN"):
    ALLOWED_HOSTS.append(os.environ.get("UCLAPI_DOMAIN"))

# If we are running under the AWS Elastic Load Balancer then enable internal
# requests so that the ELB and Health Checks work
if strtobool(os.environ.get("UCLAPI_RUNNING_ON_AWS_ELB", "False")):
    EC2_PRIVATE_IP = None
    try:
        EC2_PRIVATE_IP = requests.get("http://169.254.169.254/latest/meta-data/local-ipv4", timeout=0.01).text
    except requests.exceptions.RequestException:
        pass

    if EC2_PRIVATE_IP:
        ALLOWED_HOSTS.append(EC2_PRIVATE_IP)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'dashboard',
    'roombookings',
    'opbeat.contrib.django',
    'raven.contrib.django.raven_compat',
    'corsheaders'
]

MIDDLEWARE = [
    'opbeat.contrib.django.middleware.OpbeatAPMMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG:
    MIDDLEWARE.append(
        'dashboard.middleware.fake_shibboleth_middleware'
        '.FakeShibbolethMiddleWare'
    )

ROOT_URLCONF = 'uclapi.urls'

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

WSGI_APPLICATION = 'uclapi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get("DB_UCLAPI_NAME"),
        'USER': os.environ.get("DB_UCLAPI_USERNAME"),
        'PASSWORD': os.environ.get("DB_UCLAPI_PASSWORD"),
        'HOST': os.environ.get("DB_UCLAPI_HOST"),
        'PORT': os.environ.get("DB_UCLAPI_PORT")
    },
    'roombookings': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': os.environ.get("DB_ROOMS_NAME"),
        'USER': os.environ.get("DB_ROOMS_USERNAME"),
        'PASSWORD': os.environ.get("DB_ROOMS_PASSWORD"),
        'HOST': '',
        'PORT': ''
    },
    'gencache': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get("DB_CACHE_NAME"),
        'USER': os.environ.get("DB_CACHE_USERNAME"),
        'PASSWORD': os.environ.get("DB_CACHE_PASSWORD"),
        'HOST': os.environ.get("DB_CACHE_HOST"),
        'PORT': os.environ.get("DB_CACHE_PORT")
    }
}

DATABASE_ROUTERS = ['uclapi.dbrouters.ModelRouter']

# analytics
OPBEAT = {
    'ORGANIZATION_ID': os.environ.get("OPBEAT_ORG_ID"),
    'APP_ID': os.environ.get("OPBEAT_APP_ID"),
    'SECRET_TOKEN': os.environ.get("OPBEAT_SECRET_TOKEN")
}

RAVEN_CONFIG = {
    'dsn': os.environ.get("SENTRY_DSN"),
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "images"),
]

# Cross Origin settings
CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r'^/roombookings/.*$'

# Fair use policy
with open(os.path.join(BASE_DIR, 'uclapi/UCLAPIAcceptableUsePolicy.txt'), 'r', encoding='utf-8') as fp:
    FAIR_USE_POLICY = list(fp)

REDIS_UCLAPI_HOST = os.environ.get("REDIS_UCLAPI_HOST")
