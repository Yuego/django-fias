#coding: utf-8
from __future__ import unicode_literals, absolute_import

import datetime
from fias.importer.log import log
from lxml import etree

today = datetime.date.today()


def _fast_iter(context, func):
    for event, elem in context:
        func(elem)
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]
    del context


class LoaderBase(object):

    def __init__(self, table, version):
        self._table = table
        self._version = version
        self._today = today
        self._bulk = None
        self._model = None
        self._init()

    def _init(self):
        raise NotImplementedError()

    @staticmethod
    def _str_to_date(s):
        return datetime.datetime.strptime(s, "%Y-%m-%d").date()

    def process_row(self, row):
        raise NotImplementedError()

    def load(self, truncate=False, update=False):
        log.info('{0} table `{1}` to ver. {2}...'.format('Updating' if update else 'Filling',
                                                         self._table.full_name,
                                                         self._version.ver))

        if truncate:
            self._model.objects.all().delete()

        if not update:
            self._bulk.mode = 'fill'
        else:
            self._bulk.mode = 'update'
            self._bulk.reset_counters()

        context = etree.iterparse(self._table.open())
        _fast_iter(context=context, func=self.process_row)

        self._bulk.finish()

        log.info('Processing table `{0}` is finished'.format(self._table.full_name))
