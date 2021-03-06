"""
Django settings for Image project.

Generated by 'django-admin startproject' using Django 1.10.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$7iqxd1d-n%4(y1hnp$c1cexhr!u!e#-$#&hlg*alkx()&86wk'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Image_data',
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

ROOT_URLCONF = 'Image.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'Image_data/template')],
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

WSGI_APPLICATION = 'Image.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
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

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

TWITTER_APP_KEY = "fqXulhBIqTrZUOjeRNlcVPlMy"
TWITTER_APP_SECRET = "EgJfXTMZU3L6WD0ZKqw4DgrFBldOGSLCzmKcuVvPnCeNpByrfM"
TWITTER_TOKEN = "789411527216422912-Tu5vjkWifHPmCzqf7xPetRD9jcH9jB8"
TWITTER_SECRET = "at2IEdlItVmRwb2RBtgcQpXFmouv18n7TrFR7ykOWg590"

YOUTUBE_APP_KEY = "AIzaSyCqfkmXgsMhlF7zsrQTQD-PinO2tlBciWs"
FACEBOOK_APP_KEY = "818766041597574"
FACEBOOK_APP_SECRET = "a0b1498fdde5c082d48628247e199522"

LINKEDIN_APP_KEY = "81sjdl5x68fh6d"
LINKEDIN_APP_SECRET = "jvg1uw3ofirosAw7"
LINKEDIN_TOKEN = "AQW3FgzQgSoXiwuSyT8usi74Pbl1DkxOpc5O8Urnr9eWGRDHHqNIE9eWZAR-iNM19UIiSPCjQiTCwGRwA9BfNrWQaf2txmAbokc5tE4D6EAJAMyLyi6n0PyUHyjjJofMJwX9nm5FytP-gPjMQZZPGhlJCDGqwJ760r01LrYFz98xb9AAGqI"

