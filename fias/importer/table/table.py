# coding: utf-8
from __future__ import unicode_literals, absolute_import

try:
    from functools import reduce
except ImportError:
    pass  # Python 2 builtin reduce

from django.db import connections, router

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

name_trans = {
    'nordoc': 'normdoc',
}


class BadTableError(Exception):
    pass


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

        item = self.model(**row)
        for filter in TABLE_ROW_FILTERS:
            if item is None:
                break

            item = filter(item)

        return item

    def __next__(self):
        return self.get_next()

    next = __next__


class Table(object):
    name = None
    deleted = False
    iterator = TableIterator

    def __init__(self, filename, **kwargs):
        self.filename = filename

        name = kwargs['name'].lower()

        self.name = name_trans.get(name, name)
        self.model = table_names.get(self.name)

        self.deleted = bool(kwargs.get('deleted', False))

    def _truncate(self, model):
        db_table = model._meta.db_table
        connection = connections[router.db_for_write(model)]
        cursor = connection.cursor()

        if connection.vendor == 'postgresql':
            cursor.execute('TRUNCATE TABLE {0} RESTART IDENTITY CASCADE'.format(db_table))
        elif connection.vendor == 'mysql':
            cursor.execute('TRUNCATE TABLE `{0}`'.format(db_table))
        else:
            cursor.execute('DELETE FROM {0}'.format(db_table))

    def truncate(self):
        self._truncate(self.model)

    def open(self, tablelist):
        return tablelist.open(self.filename)

    def rows(self, tablelist):
        raise NotImplementedError()
