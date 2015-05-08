"""
Django settings for hitmeup project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['HMU_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('HMU_DEBUG', False) == 'True'

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    # Stock
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Vendor
    'django_jinja',
    'restless',

    # Custom
    'hitmeup',
    'dynamic_components',
    'static_pages',
    'user_accounts',
    'ourcalendar',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'hitmeup.urls'

CONTEXT_PROCESSORS = [
    # Stock
    "django.contrib.auth.context_processors.auth",
    "django.template.context_processors.debug",
    "django.template.context_processors.i18n",
    "django.template.context_processors.media",
    "django.template.context_processors.static",
    "django.template.context_processors.tz",
    "django.contrib.messages.context_processors.messages",

    # Custom
    'dynamic_components.context_processors.navbar',
]

TEMPLATES = [
    {
        'BACKEND': "django_jinja.backend.Jinja2",
        'APP_DIRS': True,
        'OPTIONS': {
            'match_extension': '.jinja',

            "newstyle_gettext": True,
            "extensions": [
                "jinja2.ext.do",
                "jinja2.ext.loopcontrols",
                "jinja2.ext.with_",
                "jinja2.ext.i18n",
                "jinja2.ext.autoescape",
                "django_jinja.builtins.extensions.CsrfExtension",
                "django_jinja.builtins.extensions.CacheExtension",
                "django_jinja.builtins.extensions.TimezoneExtension",
                "django_jinja.builtins.extensions.UrlsExtension",
                "django_jinja.builtins.extensions.StaticFilesExtension",
                "django_jinja.builtins.extensions.DjangoFiltersExtension",
            ],
            "autoescape": True,
            "auto_reload": DEBUG,
            "translation_engine": "django.utils.translation",
            'context_processors': CONTEXT_PROCESSORS,
        }
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': CONTEXT_PROCESSORS,
        },
    },
]

WSGI_APPLICATION = 'hitmeup.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

import dj_database_url

DATABASES = {
    'default': dj_database_url.config()
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_ROOT = 'staticroot'

STATIC_URL = '/static/'

# Navigation

from navigation import entries

NAVBAR_ENTRIES = entries

# Scaffold command

SCAFFOLDAPP_DIRS = [
    (os.path.join('{app}', 'static'), "holds project static assets"),
    (os.path.join('{app}', 'static', '{app}'), "holds {app}'s static assets"),
    (os.path.join('{app}', 'static', '{app}', 'js'), "holds {app}'s Javascript files"),
    (os.path.join('{app}', 'static', '{app}', 'css'), "holds {app}'s CSS files"),
    (os.path.join('{app}', 'static', '{app}', 'img'), "holds {app}'s image files"),
    (os.path.join('{app}', 'templates'), "holds project templates"),
    (os.path.join('{app}', 'templates', '{app}'), "holds {app}'s templates"),
]

SCAFFOLDAPP_FILES = [
    (os.path.join('{app}', 'urls.py'), "describes {app}'s routes"),
]

# Authentication
LOGIN_URL = '/login/'
