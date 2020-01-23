"""
WSGI config for huidetang project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "huidetang.settings.localhost")
import pymysql

pymysql.install_as_MySQLdb()
pymysql.version_info = (1, 3, 13, 'final', 0)

application = get_wsgi_application()
