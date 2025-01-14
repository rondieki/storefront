"""
Django settings for storefront project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-jk!kb5ipi=c)g=bnn#uw-e0$_p$8eaceoq3lribtfdgx%=@#*3'

STRIPE_PUBLISHABLE_KEY = 'pk_test_51OxC8A03R5ykTtcCPFGoH8QA4TQg8OeNJeyxXOlQZL4L4NaZGwS0lf59w3WfY9BS7JAd2s2AfadVs4VUOX1jHW6C00GQ3jm0DR'
STRIPE_SECRET_KEY = 'sk_test_51OxC8A03R5ykTtcCtg47DdGj4SxU9Sw3CaA3G2fqDC2bve0eUYRCisVx7jzKxlfklE38IZ26BgvCcknASJh5dgci00iTqU0mJj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '2d84-102-213-93-18.ngrok-free.app',  # Add the ngrok hostname
    'localhost',  # Add localhost if needed
    '127.0.0.1',  # Add localhost IP if needed
]


# Application definition

INSTALLED_APPS = [
    'playground',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_admin_filter',
    'django_daraja',
    
]

AUTHENTICATION_BACKENDS=[
    'django.contrib.auth.backends.ModelBackend'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'storefront.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'storefront.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'kartngo1', 
#         'USER': 'postgres',   
#         'PASSWORD': 'welcome', 
#         'HOST': 'localhost',
#         'PORT': '5433',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'playground/static')
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# settings.py
AUTH_USER_MODEL = 'auth.User'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Mpesa configs

MPESA_ENVIRONMENT = "sandbox"

# Define M-Pesa API credentials
MPESA_CONSUMER_KEY = "wNjIICFzH4wReyZwd9JVqUlGzynl3OYPGHbgpCXuhM3X5S26"
MPESA_CONSUMER_SECRET = "V8A9yuDSMw3RsJ5tZJlnNxsBxeBJdCttyKyyy3Kel59a3cdONZXnjIRVL2NCgQuN"
MPESA_SHORTCODE = "174379"
MPESA_EXPRESS_SHORTCODE = "174379"
MPESA_SHORTCODE_TYPE = "YOUR_MPESA_SHORTCODE"
MPESA_PASSKEY = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"

# Define M-Pesa API URLs
MPESA_OAUTH_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
MPESA_STK_PUSH_URL = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

MPESA_INITIATOR_USERNAME = "testapi"

MPESA_INITIATOR_SECURITY_CREDENTIAL = "Safaricom999!*!"