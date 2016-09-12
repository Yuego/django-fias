# coding: utf-8
from __future__ import unicode_literals, absolute_import

from fias.models import Version

from fias.importer.signals import pre_load, post_load
from fias.importer.table import TableFactory

from .wrapper import SourceWrapper


class TableListLoadingError(Exception):
    pass


class TableList(object):
    wrapper_class = SourceWrapper
    wrapper = None

    table_list = None
    date = None
    version_info = None

    def __init__(self, src, version=None, tempdir=None):
        self.info_version = version
        self.src = src
        self.tempdir = tempdir

        if version is not None:
            assert isinstance(version, Version), 'version must be an instance of Version model'

            self.date = version.dumpdate

        pre_load.send(sender=self.__class__, src=src)
        self.wrapper = self.load_data(src)
        post_load.send(sender=self.__class__, wrapper=self.wrapper)

    def load_data(self, source):
        return self.wrapper_class(source=source)

    def get_table_list(self):
        return self.wrapper.get_file_list()

    @property
    def tables(self):
        if self.table_list is None:
            self.table_list = {}
            for filename in self.get_table_list():
                table = TableFactory.parse(filename=filename)
                if table is None:
                    continue
                self.table_list.setdefault(table.name, []).append(table)

        return self.table_list

    def get_date_info(self, name):
        return self.wrapper.get_date_info(filename=name)

    @property
    def dump_date(self):
        if self.date is None:
            first_name = self.get_table_list()[0]
            self.date = self.get_date_info(first_name)

        return self.date

    def open(self, filename):
        return self.wrapper.open(filename=filename)

    @property
    def version(self):
        if self.version_info is None:
            self.version_info = Version.objects.nearest_by_date(self.dump_date)
        return self.version_info
