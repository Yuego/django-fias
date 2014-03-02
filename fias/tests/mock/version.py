#coding: utf-8
from __future__ import unicode_literals, absolute_import

from .table import get_table_date


class Version(object):

    def __init__(self, ver=0):
        self.ver = ver
        self.dumpdate = get_table_date()
        self.date = None
        self.complete_xml_url = ''
        self.delta_xml_url = ''
