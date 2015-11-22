#coding: utf-8
from __future__ import unicode_literals, absolute_import

import datetime
import os

from .tablelist import TableList, TableListLoadingError


class EmptyDirError(TableListLoadingError):
    pass


class DirectoryTableList(TableList):

    def __init__(self, src, version=None, raw=False):
        self._list = None
        super(DirectoryTableList, self).__init__(src=src, version=version, raw=raw)

    def get_tables_list(self):
        if self._list is None:
            self._list = [f for f in os.listdir(self.source) if os.path.isfile(os.path.join(self.source, f))]
        return self._list

    def get_full_path(self, filename):
        return os.path.join(self.source, filename)

    def open(self, filename):
        return open(self.get_full_path(filename), 'rb')

    def get_date_info(self, name):
        st = os.stat(os.path.join(self.source, name))
        return datetime.datetime.fromtimestamp(st.st_mtime)

