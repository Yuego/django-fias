#coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

_FIAS_TABLES_DEFAULT = ['socrbase', 'normdoc', 'addrobj', 'house']

FIAS_TABLES = getattr(settings, 'FIAS_TABLES', _FIAS_TABLES_DEFAULT)

FIAS_DATABASE_ALIAS = getattr(settings, 'FIAS_DATABASE_ALIAS', 'fias')

# Чтобы использовать для данных ФИАС другую базу данных,
# добавьте роутер 'django_fias.routers.FIASRouter' в список `DATABASE_ROUTERS`