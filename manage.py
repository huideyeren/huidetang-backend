#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "huidetang.settings.localhost")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

    import pymysql

    pymysql.install_as_MySQLdb()
    pymysql.version_info = (1, 3, 13, 'final', 0)
