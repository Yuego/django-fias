# coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db.utils import DEFAULT_DB_ALIAS
from django.utils.module_loading import import_module
from fias.weights import weights

_DEFAULT = ('normdoc', 'landmark', 'houseint', 'house')

TABLES = ['socrbase', 'addrobj']
TABLES.extend([x.lower() for x in set(getattr(settings, 'FIAS_TABLES', [])) if x.lower() in _DEFAULT])

DELETED_TABLES = ('addrobj', 'house', 'houseint', 'normdoc')


DATABASE_ALIAS = getattr(settings, 'FIAS_DATABASE_ALIAS', DEFAULT_DB_ALIAS)

if DATABASE_ALIAS not in settings.DATABASES:
    raise ImproperlyConfigured('FIAS: database alias `{0}` was not found in DATABASES'.format(DATABASE_ALIAS))
elif DATABASE_ALIAS != DEFAULT_DB_ALIAS and 'fias.routers.FIASRouter' not in settings.DATABASE_ROUTERS:
    raise ImproperlyConfigured('FIAS: for use external database add `fias.routers.FIASRouter`'
                               ' into `DATABASE_ROUTERS` list in your settings.py')

user_weights = getattr(settings, 'FIAS_SB_WEIGHTS', {})
if not isinstance(user_weights, dict):
    raise ImproperlyConfigured('FIAS_SB_WEIGHTS should be a dict type')

weights.update(user_weights)


"""
см. fias.importer.filters
указывается список путей к функциям-фильтрам
фильтры применяются к *каждому* объекту
один за другим, пока не закончатся,
либо пока какой-нибудь из них не вернёт None
если фильтр вернул None, объект не импортируется в БД

пример:

FIAS_TABLE_ROW_FILTERS = [
    'fias.importer.filters.example_filter_accept',
]
"""
row_filters = getattr(settings, 'FIAS_TABLE_ROW_FILTERS', [])
TABLE_ROW_FILTERS = []
for flt_path in row_filters:
    try:
        flt = import_module(flt_path)
    except ImportError:
        raise ImproperlyConfigured('Table row filter module `{0}` does not exists'.format(flt_path))
    else:
        TABLE_ROW_FILTERS.append(flt)

SUGGEST_BACKEND = getattr(settings, 'FIAS_SUGGEST_BACKEND', 'fias.suggest.backends.noop')
SUGGEST_VIEW = getattr(settings, 'FIAS_SUGGEST_VIEW', 'fias:suggest')
SUGGEST_AREA_VIEW = getattr(settings, 'FIAS_SUGGEST_AREA_VIEW', 'fias:suggest-area')
