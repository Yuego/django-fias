#coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.conf import settings

from sphinxit.core.helpers import BaseSearchConfig
from sphinxit.core.processor import Search

from fias.config import FIAS_SPHINX_ADDROBJ_INDEX

class SphinxItConfig(BaseSearchConfig):
    DEBUG = settings.DEBUG
    WITH_STATUS = False
    WITH_META = False
    SEARCHD_CONNECTION = getattr(settings, 'FIAS_SEARCHD_CONNECTION', {
        'host': '127.0.0.1',
        'port': 9306,
    })


def _get_search():
    return Search(indexes=[FIAS_SPHINX_ADDROBJ_INDEX], config=SphinxItConfig)

search = _get_search
