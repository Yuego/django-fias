#coding: utf-8
from __future__ import unicode_literals, absolute_import

import datetime
from django.db import connection, connections, router
from fias.importer.log import log
from lxml import etree

today = datetime.date.today()
_bom_header = b'\xef\xbb\xbf'

def _fast_iter(context, func):
    for event, elem in context:
        func(elem)
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]
    del context


class LoaderBase(object):

    def __init__(self, table):
        self._table = table
        self._today = today
        self._bulk = None
        self._model = None
        self._init()

    def _init(self):
        raise NotImplementedError()

    def _truncate(self):
        db_table = self._model._meta.db_table
        cursor = connections[router.db_for_write(self._model)].cursor()

        if connection.vendor == 'postgresql':
            cursor.execute('TRUNCATE TABLE {0} RESTART IDENTITY CASCADE'.format(db_table))
        elif connection.vendor == 'mysql':
            cursor.execute('TRUNCATE TABLE `{0}`'.format(db_table))
        else:
            cursor.execute('DELETE FROM {0}'.format(db_table))

    @staticmethod
    def _str_to_date(s):
        return datetime.datetime.strptime(s, "%Y-%m-%d").date()

    def process_row(self, row):
        raise NotImplementedError()

    def load(self, truncate=False, update=False):
        if truncate:
            self._truncate()

        if update:
            self._bulk.mode = 'update'
            self._bulk.reset_counters()
        else:
            self._bulk.mode = 'fill'

        # workaround for XMLSyntaxError: Document is empty, line 1, column 1
        xml = self._table.open()
        bom = xml.read(3)
        if bom != _bom_header:
            xml = self._table.open()
        else:
            log.info('Fixed wrong BOM header')

        context = etree.iterparse(xml)

        _fast_iter(context=context, func=self.process_row)

        self._bulk.finish()

        log.info('Processing table `{0}` is finished'.format(self._table.full_name))
