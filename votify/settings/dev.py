from .base import *

DEBUG = TEMPLATE_DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'dev.db',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Disable caching while in development
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# set up devserver if installed
# try:
#     import devserver
#     INSTALLED_APPS += (
#         'devserver',
#     )
# except ImportError:
#     pass

# Don't use Sentry logging even if configured for production
LOGGING = BASE_LOGGING
