import os
from .base_settings import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('MYBLOG_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    'www.lyangly.xyz',
]

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('MYBLOG_DATABASE_ENGINE'),
        'NAME': os.environ.get('MYBLOG_DATABASE_NAME'),
        'USER': os.environ.get('MYBLOG_DB_USER'),
        'PASSWORD': os.environ.get('MYBLOG_DB_PASS'),
        'HOST': '127.0.0.1',
        'PORT': 5432
    }
}

# Cache settings
CACHES = {
    'default': {
        "BACKEND": "django_redis.cache.RedisCache",
        # "LOCATION": "redis://127.0.0.1:6379/1",
        "LOCATION": "unix:/home/myblog/docker/redis/data/redis.sock?db=1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Use redis as session's backend
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# Mail settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('SEND_MAIL_HOST')
EMAIL_HOST_USER = os.environ.get('SEND_EMAIL_USER')
EMAIL_HOST_PASSWORD = os.environ.get('SEND_MAIL_PASS')
EMAIL_PORT = int(os.environ.get('SEND_MAIL_PORT'))
EMAIL_USE_TLS = True

# Admin email
ADMINS = (('admin', 'lyangly@live.com'), )

# Logging module
LOGGIN = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/var/log/myblog_debug.log',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        }
    }
}