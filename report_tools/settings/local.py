from .base import *
from logging.config import dictConfig

DEBUG = True

SECRET_KEY = 'l#+ea&m+y_^_098iy8e*$9-al1z72u9qalig^*hx=e^8ij#+b@'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INSTALLED_APPS.extend(['debug_toolbar', 'sslserver'])
MIDDLEWARE_CLASSES.extend(['debug_toolbar.middleware.DebugToolbarMiddleware'])

# For Django Debug Toolbar:
INTERNAL_IPS = ('127.0.0.1', '10.0.2.2',)
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

# Logging

# Log to console instead of a file when running locally
LOGGING['handlers']['default'] = {
    'level': logging.DEBUG,
    'class': 'logging.StreamHandler',
    'formatter': 'simple',
}

# Log calls to sdk
LOGGING['loggers']['canvas_sdk'] = {
    'level': logging.DEBUG,
    'handlers': ['default'],
    'propagate': False,
}

dictConfig(LOGGING)
