from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

STATIC_ROOT = normpath(join(SITE_ROOT, 'http_static'))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': 'isitedev',
        'USER': SECURE_SETTINGS['DJANGO_DB_USER'],
        'PASSWORD': SECURE_SETTINGS['DJANGO_DB_PASS'],
        'HOST': 'icd3.isites.harvard.edu',
        'PORT': '8103',
        'OPTIONS': {
            'threaded': True,
        },
        'CONN_MAX_AGE': 600,
    }
}