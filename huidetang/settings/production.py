from .base import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'huidetang',
        'USER': os.getenv("DJANGO_STAGING_USER"),
        'PASSWORD': os.getenv("DJANGO_STAGING_PASSWORD"),
        'HOST': os.getenv("DJANGO_STAGING_HOST"),
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'connect_timeout': 28800,

        },
        'TEST': {
            'NAME': 'test_huidetang'
        }
    }
}

try:
    from .local import *
except ImportError:
    pass

