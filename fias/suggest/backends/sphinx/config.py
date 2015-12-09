# coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.conf import settings
from fias.config import DATABASE_ALIAS

SPHINX_ADDROBJ_INDEX_NAME = getattr(settings, 'FIAS_SPHINX_ADDROBJ_INDEX_NAME', 'addrobj')

SPHINX_ADDROBJ_INDEX = DATABASE_ALIAS + '_' + SPHINX_ADDROBJ_INDEX_NAME


SEARCHD_CONNECTION = {
    'ENGINE': 'django.db.backends.mysql',
    'host': '127.0.0.1',
    'port': 9306,
}
SEARCHD_CONNECTION.update(getattr(settings, 'FIAS_SEARCHD_CONNECTION', {}))
