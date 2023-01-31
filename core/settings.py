"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from datetime import timedelta
from pathlib import Path
from typing import List

from dotenv import load_dotenv

load_dotenv()

APPEND_SLASH = True

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY: str = os.environ.get("DJANGO_SECRET_KEY", "INSECURE")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG: bool = True if os.environ.get('DEBUG') == '1' else False

ALLOWED_HOSTS: List = [
    '192.168.0.20',
    '127.0.0.1'
]

# Application definition
INSTALLED_APPS: list[str] = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt',
    'users',
    'ecommerce',
    'payments',
    'cart',
]

MIDDLEWARE: list[str] = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

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
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # noqa :E501
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # noqa :E501
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # noqa :E501
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # noqa :E501
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Fortaleza'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = 'static'
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ORIGIN_WHITELIST: list[str] = [
    'http://localhost:3000',
    'http://192.168.0.20:3000',
]


AUTH_USER_MODEL = 'users.User'

# REST CONFIGS

REST_FRAMEWORK = {
    'PAGE_SIZE': os.environ.get('PAGE_SIZE') or 12,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination'  # noqa: E501
}

# JWT CONFIGS

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=4),
    'REFRESH_TOKEN_LIFETIME': timedelta(hours=16),
    'BLACKLIST_AFTER_ROTATION': False,

    'SIGNING_KEY': os.environ.get('JWT_SECRET_KEY'),

    'AUTH_HEADER_TYPES': ('Bearer',),
}

# Media

MEDIA_URL: str = 'media/'
MEDIA_ROOT: Path = BASE_DIR / 'media/'

# SMTP

# DEFAULT_BACKEND
EMAIL_BACKEND: str | None = os.environ.get('EMAIL_BACKEND')
# Email sender
DEFAULT_FROM_EMAIL: str = 'britodavi122@gmail.com'
# Client Host for send emails
EMAIL_HOST: str | None = os.environ.get('EMAIL_HOST')
# TLS Port
EMAIL_PORT: str | None = os.environ.get('EMAIL_PORT')
# Use TLS
EMAIL_USE_TLS: str | None = os.environ.get('EMAIL_USE_TLS')
# Email to send email
EMAIL_HOST_USER: str | None = os.environ.get('EMAIL_HOST_USER')
# Email Password
EMAIL_HOST_PASSWORD: str | None = os.environ.get('EMAIL_HOST_PASSWORD')


# Default Password Reset Timeout

PASSWORD_RESET_TIMEOUT: float = 60 * 30

# CACHE

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get('REDIS_CACHE_LOCATION'),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "TIMEOUT": 60 * 5,
        "KEY_PREFIX": '',
    }
}

SESSION_ENGINE: str = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS: str = "default"
