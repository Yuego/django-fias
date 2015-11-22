#coding: utf-8
from __future__ import unicode_literals, absolute_import

from fias.models import Version
from ..table import TableFactory

class TableListLoadingError(Exception):
    pass


class TableList(object):
    def __init__(self, path, version=None, raw=False):
        self._version = version
        self._path = path
        self._raw = raw

        if self._version is not None:
            self._date = self._version.dumpdate
        else:
            self._date = None

        self._tables = None
        self.load(path)

    def load(self, path):
        raise NotImplementedError()

    def get_tables_list(self):
        raise NotImplementedError()

    @property
    def tables(self):
        if self._tables is None:
            self._tables = {}
            for filename in self.get_tables_list():
                table = TableFactory.parse(filename=filename, raw=self._raw)
                self._tables.setdefault(table.name, []).append(table)

        return self._tables

    @property
    def dump_date(self):
        raise NotImplementedError()

    def open(self, filename):
        raise NotImplementedError()

    @property
    def version(self):
        if self._version is None:
            self._version = Version.objects.nearest_by_date(self.dump_date)
        return self._version
