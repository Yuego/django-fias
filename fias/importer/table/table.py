#coding: utf-8
from __future__ import unicode_literals, absolute_import

try:
    from functools import reduce
except ImportError:
    pass # Python 2 builtin reduce

from fias.config import TABLE_ROW_FILTERS
from fias.models import (
    AddrObj,
    House, HouseInt,
    LandMark,
    NormDoc,
    SocrBase,
)

table_names = {
    'addrobj': AddrObj,
    'house': House,
    'houseint': HouseInt,
    'landmark': LandMark,
    'normdoc': NormDoc,
    'socrbase': SocrBase,
}


class ParentLookupException(Exception):
    pass


class TableIterator(object):

    def __init__(self, fd, model):
        self._fd = fd
        self.model = model

    def __iter__(self):
        if self.model is None:
            return []

        return self

    def get_context(self):
        raise NotImplementedError()

    def get_next(self):
        raise NotImplementedError()

    def format_row(self, row):
        raise NotImplementedError()

    def process_row(self, row):
        try:
            row = dict(self.format_row(row))
        except ParentLookupException as e:
            return None

        return reduce(lambda a, x: x(a) if a is not None else a, TABLE_ROW_FILTERS, self.model(**row))

    def __next__(self):
        return self.get_next()

    next = __next__


class Table(object):
    name = None
    iterator = TableIterator

    def __init__(self, filename, **kwargs):
        self.filename = filename

        self.name = kwargs['name'].lower()
        self.model = table_names.get(self.name, None)

    def open(self, tablelist):
        return tablelist.open(self.filename)

    def rows(self, tablelist):
        raise NotImplementedError()
