"""
Django settings for report_tools project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
import os
from os.path import abspath, basename, dirname, join, normpath
from sys import path
from .secure import SECURE_SETTINGS
from django.core.urlresolvers import reverse_lazy
import logging
import time

# Normally you should not import ANYTHING from Django directly
# into your settings, but ImproperlyConfigured is an exception.
from django.core.exceptions import ImproperlyConfigured

def get_env_variable(var_name):
    """ Get the environment variable or return exception """
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the %s environment variable" % var_name
        raise ImproperlyConfigured(error_msg)


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = dirname(dirname(__file__))

# Path stuff as recommended by Two Scoops / with local mods

# Absolute filesystem path to the Django project config directory:
# (this is the parent of the directory where this file resides, 
# since this file is now inside a 'settings' pacakge directory)
DJANGO_PROJECT_CONFIG = dirname(dirname(abspath(__file__)))

# Absolute filesystem path to the top-level project folder:
# (this is one directory up from the project config directory)
SITE_ROOT = dirname(DJANGO_PROJECT_CONFIG)

# Site name:
SITE_NAME = basename(SITE_ROOT)

# Add our project to our pythonpath, this way we don't need to type our project
# name in our dotted import paths:
path.append(SITE_ROOT)

# End path stuff

SECRET_KEY = SECURE_SETTINGS.get('django_secret_key')

DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'icommons_ui',
    'icommons_common',
    'account_courses',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_auth_lti.middleware.LTIAuthMiddleware',

)

ROOT_URLCONF = 'report_tools.urls'

WSGI_APPLICATION = 'report_tools.wsgi.application'

AUTHENTICATION_BACKENDS = (
    'django_auth_lti.backends.LTIAuthBackend',
)

LOGIN_URL = reverse_lazy('lti_auth_error')

LTI_OAUTH_CREDENTIALS = SECURE_SETTINGS.get('lti_oauth_credentials', None)


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': SECURE_SETTINGS.get('db_default_name'),
        'USER': SECURE_SETTINGS.get('db_default_user'),
        'PASSWORD': SECURE_SETTINGS.get('db_default_password'),
        'HOST': SECURE_SETTINGS.get('db_default_host'),
        'PORT': SECURE_SETTINGS.get('db_default_port'),  # Default postgres port
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/reports/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    normpath(join(SITE_ROOT, 'static')),
)

STATIC_ROOT = normpath(join(SITE_ROOT, 'http_static'))

REPORT_TOOLS = {
    'canvas_client_id': SECURE_SETTINGS['client_id'],
    'canvas_client_key': SECURE_SETTINGS['client_secret'],
}

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Logging

LOG_ROOT = SECURE_SETTINGS.get('log_root', '')  # Default to current directory

# Make sure log timestamps are in GMT
logging.Formatter.converter = time.gmtime


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(message)s'
        }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        # Log to a text file that can be rotated by logrotate
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': join(LOG_ROOT, 'django-report_tools.log'),
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['logfile'],
            'level': SECURE_SETTINGS.get('log_level', 'INFO'),        
            'propagate': True,
        },
        'django': {
            'handlers': ['logfile'],
            'level': SECURE_SETTINGS.get('log_level', 'INFO'),        
            'propagate': True,
        },
        'report_tools': {
            'handlers': ['logfile'],
            'level': SECURE_SETTINGS.get('log_level', 'INFO'),        
            'propagate': True,
        },
    }
}
