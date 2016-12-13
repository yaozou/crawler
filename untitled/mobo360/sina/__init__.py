import pymysql
import os
import django

pymysql.install_as_MySQLdb()
os.environ['DJANGO_SETTINGS_MODULE'] = 'untitled.settings'
if django.VERSION >= (1,7):
    django.setup()
