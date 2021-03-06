"""
Django settings for report_tools project.
Generated by 'django-admin startproject' using Django 1.9 of TLT template.
For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import logging
from datetime import timedelta

from django.core.urlresolvers import reverse_lazy

from .secure import SECURE_SETTINGS

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# NOTE: Since we have a settings module, we have to go one more directory up to
# get to the project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_auth_lti',
    'icommons_ui',
    'account_courses',
    'canvas_oauth.apps.CanvasOAuthConfig',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #  'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_auth_lti.middleware.LTIAuthMiddleware',
    'canvas_oauth.middleware.OAuthMiddleware',
]

ROOT_URLCONF = 'report_tools.urls'

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

WSGI_APPLICATION = 'report_tools.wsgi.application'

# Authentication

AUTHENTICATION_BACKENDS = (
    'django_auth_lti.backends.LTIAuthBackend',
)

LOGIN_URL = reverse_lazy('lti_auth_error')

LTI_OAUTH_LAUNCH_KEY = SECURE_SETTINGS['lti_oauth_launch_key']
LTI_OAUTH_LAUNCH_SECRET = SECURE_SETTINGS['lti_oauth_launch_secret']

# This dictionary is required by the django-auth-lti library
LTI_OAUTH_CREDENTIALS = {
    LTI_OAUTH_LAUNCH_KEY: LTI_OAUTH_LAUNCH_SECRET,
}


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': SECURE_SETTINGS.get('db_default_name', 'report_tools'),
        'USER': SECURE_SETTINGS.get('db_default_user', 'postgres'),
        'PASSWORD': SECURE_SETTINGS.get('db_default_password'),
        'HOST': SECURE_SETTINGS.get('db_default_host', '127.0.0.1'),
        'PORT': SECURE_SETTINGS.get('db_default_port', 5432),  # Default postgres port
    }
}

# Cache
# https://docs.djangoproject.com/en/1.9/ref/settings/#std:setting-CACHES

REDIS_HOST = SECURE_SETTINGS.get('redis_host', '127.0.0.1')
REDIS_PORT = SECURE_SETTINGS.get('redis_port', 6379)

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': "redis://%s:%s/0" % (REDIS_HOST, REDIS_PORT),
        'OPTIONS': {
            'PARSER_CLASS': 'redis.connection.HiredisParser'
        },
        'KEY_PREFIX': 'report_tools',  # Provide a unique value for app cache
        # See following for default timeout (5 minutes as of 1.7):
        # https://docs.djangoproject.com/en/1.9/ref/settings/#std:setting-CACHES-TIMEOUT
        'TIMEOUT': SECURE_SETTINGS.get('default_cache_timeout_secs', 300),
    }
}

# Sessions
# https://docs.djangoproject.com/en/1.9/topics/http/sessions/#module-django.contrib.sessions

# Store sessions in default cache defined below
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
# NOTE: This setting only affects the session cookie, not the expiration of the
# session being stored in the cache.  The session keys will expire according to
# the value of SESSION_COOKIE_AGE (defaults to 2 weeks)
# https://docs.djangoproject.com/en/1.8/ref/settings/#session-cookie-age
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'
# A boolean that specifies whether Django's translation system should be enabled.
# This provides an easy way to turn it off, for performance. If this is set to
# False, Django will make some optimizations so as not to load the translation
# machinery.
USE_I18N = False
# A boolean that specifies if localized formatting of data will be enabled by
# default or not. If this is set to True, e.g. Django will display numbers and
# dates using the format of the current locale.  NOTE: this would only really
# come into play if your locale was outside of the US
USE_L10N = False
# A boolean that specifies if datetimes will be timezone-aware by default or not.
# If this is set to True, Django will use timezone-aware datetimes internally.
# Otherwise, Django will use naive datetimes in local time.
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_ROOT = os.path.normpath(os.path.join(BASE_DIR, 'http_static'))

STATIC_URL = '/static/'

# Logging
# https://docs.djangoproject.com/en/1.9/topics/logging/#configuring-logging

# Turn off default Django logging
# https://docs.djangoproject.com/en/1.9/topics/logging/#disabling-logging-configuration
LOGGING_CONFIG = None

_DEFAULT_LOG_LEVEL = SECURE_SETTINGS.get('log_level', logging.DEBUG)
_LOG_ROOT = SECURE_SETTINGS.get('log_root', '')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s\t%(asctime)s.%(msecs)03dZ\t%(name)s:%(lineno)s\t%(message)s',
            'datefmt': '%Y-%m-%dT%H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s\t%(name)s:%(lineno)s\t%(message)s',
        },
    },
    'handlers': {
        # By default, log to a file
        'default': {
            'class': 'logging.handlers.WatchedFileHandler',
            'level': _DEFAULT_LOG_LEVEL,
            'formatter': 'verbose',
            'filename': os.path.join(_LOG_ROOT, 'django-report_tools.log'),
        },
    },
    # This is the default logger for any apps or libraries that use the logger
    # package, but are not represented in the `loggers` dict below.  A level
    # must be set and handlers defined.  Setting this logger is equivalent to
    # setting and empty string logger in the loggers dict below, but the
    # separation here is a bit more explicit.  See link for more details:
    # https://docs.python.org/2.7/library/logging.config.html#dictionary-schema-details
    'root': {
        'level': logging.WARNING,
        'handlers': ['default'],
    },
    'loggers': {
        'django': {
            'level': _DEFAULT_LOG_LEVEL,
            'handlers': ['default'],
            'propagate': False,
        },
        'account_courses': {
            'level': _DEFAULT_LOG_LEVEL,
            'handlers': ['default'],
            'propagate': False,
        },
        'canvas_sdk': {
            'level': _DEFAULT_LOG_LEVEL,
            'handlers': ['default'],
            'propagate': False,
        },
        'canvas_oauth': {
            'level': _DEFAULT_LOG_LEVEL,
            'handlers': ['default'],
            'propagate': False,
        },
        # Make sure that propagate is False so that the root logger doesn't get
        # involved after an app logger handles a log message.
    },
}

# Other project specific settings

CANVAS_OAUTH_CLIENT_ID = SECURE_SETTINGS['canvas_client_id']
CANVAS_OAUTH_CLIENT_SECRET = SECURE_SETTINGS['canvas_client_secret']
CANVAS_OAUTH_CANVAS_DOMAIN = SECURE_SETTINGS['canvas_domain']
CANVAS_OAUTH_TOKEN_EXPIRATION_BUFFER = timedelta(minutes=3)
