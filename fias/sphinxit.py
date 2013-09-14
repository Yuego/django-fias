#coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.conf import settings


from sphinxit.core.helpers import BaseSearchConfig
from sphinxit.core.processor import Search

from fias import config as fias_config


class SphinxItConfig(BaseSearchConfig):
    DEBUG = settings.DEBUG
    WITH_STATUS = False
    WITH_META = False


def _get_search():
    return Search(indexes=['addrobj'], config=SphinxItConfig)

search = _get_search
