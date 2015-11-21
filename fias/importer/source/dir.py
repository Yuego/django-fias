#coding: utf-8
from __future__ import unicode_literals, absolute_import

import datetime

from .tablelist import TableList, TableListLoadingError


class EmptyDirError(TableListLoadingError):
    pass


class DirectoryTableList(TableList):

    def load(self, path):
        raise NotImplementedError()
