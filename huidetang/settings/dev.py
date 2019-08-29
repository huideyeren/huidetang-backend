from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3zws&s!t%xs4lec!bd&k8$l^5lr&r%xa5!kv*4eji5n-@ap#e='

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

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
