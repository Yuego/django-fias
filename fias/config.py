#coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

_DEFAULT = ('landmark', 'houseint', 'house')

FIAS_TABLES = ['socrbase', 'normdoc', 'addrobj']
FIAS_TABLES.extend([x for x in list(getattr(settings, 'FIAS_TABLES', _DEFAULT)) if x in _DEFAULT])

FIAS_DELETED_TABLES = ('addrobj', 'house', 'houseint', 'normdoc')

FIAS_DATABASE_ALIAS = getattr(settings, 'FIAS_DATABASE_ALIAS', 'fias')

# Чтобы использовать для данных ФИАС другую базу данных,
# добавьте роутер 'fias.routers.FIASRouter' в список `DATABASE_ROUTERS`