"""
Django settings for yatube project.

Generated by 'django-admin startproject' using Django 2.2.19.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'n=v#=fk6yf^yn6!&$(0n=fj2o%jg9l%x7uig^ezplg+ww-=-xl'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '*',
]


# Application definition

INSTALLED_APPS = [
    'storage',
    'tasks',
    'tests',
    'corresp',
    'posts',
    'about',
    'users',
    'configs',
    'passes',
    'pro',
    'background_task',
    'sorl.thumbnail',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'yatube.urls'
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
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

WSGI_APPLICATION = 'yatube.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

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


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'  # 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = '/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'posts/static')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'posts/static'),
]

LOGIN_URL = '/auth/login/'
LOGIN_REDIRECT_URL = '/auth/users/0/'
# LOGIN_REDIRECT_URL = '/calendar/0/'
# LOGOUT_REDIRECT_URL = 'index'

#  подключаем движок filebased.EmailBackend
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# указываем директорию, в которую будут складываться файлы писем
EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails")

POSTS_IN_PAGE = 14
RIGHTS = {
    'dmitry.mylnikov',
    'Konstantin.Mishukov',
    'yaroslav.bogdanov',
    'ekaterina.mikheeva',
}
STORAGE_RIGHTS = {}
SADEC_RIGHTS = {}
PASSES_RIGHTS = {}
PRO_RIGHTS = {}

# EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_HOST = 'mail.uac-ic.ru'
EMAIL_PORT = 25
# EMAIL_HOST_USER = "*******@yandex.ru"
# EMAIL_HOST_PASSWORD = "C*******"
# EMAIL_HOST_USER = 'nikolay.emelyanov@ic.irkut.com'
EMAIL_HOST_USER = 'rrz@ic.irkut.com'
EMAIL_HOST_PASSWORD = 'Oc@dD2_AUR'
# EMAIL_USE_TLS = False
# EMAIL_USE_SSL = True
SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
