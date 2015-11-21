#coding: utf-8
from __future__ import unicode_literals, absolute_import

import datetime
import rarfile
from progress.bar import Bar

try:
    from urllib import urlretrieve
except ImportError:
    from urllib.request import urlretrieve

from .tablelist import TableList, TableListLoadingError

rarfile.UNRAR_TOOL = 'unrar'


class BadArchiveError(TableListLoadingError):
    pass


class LocalArchiveTableList(TableList):

    def __init__(self, path):
        self._archive = None
        super(LocalArchiveTableList, self).__init__(path)

    def load(self, path):
        try:
            self._archive = rarfile.RarFile(path)
        except (rarfile.NotRarFile, rarfile.BadRarFile) as e:
            raise BadArchiveError('Archive: `{0}`, ver: `{1}` corrupted'
                                  ' or is not rar-archive'.format(path))

        if not self._archive.namelist():
            raise BadArchiveError('Archive: `{0}`, ver: `{1}` is empty'
                                  ''.format(path))

    def get_tables_list(self):
        return self._archive.namelist()

    @property
    def dump_date(self):
        if self._date is None:
            first_name = self._archive.namelist()[0]
            info = self._archive.getinfo(first_name)
            self._date = datetime.date(*info.date_time[0:3])

        return self._date

    def open(self, filename):
        return self._archive.open(filename)


class DlProgressBar(Bar):
    message = 'Downloading: '
    suffix = '%(index)d/%(max)d'
    hide_cursor = False


class RemoteArchiveTableList(LocalArchiveTableList):

    def load(self, path):
        progress = DlProgressBar()

        def update_progress(count, block_size, total_size):
            progress.goto(int(count * block_size * 100 / total_size))

        path = urlretrieve(path, reporthook=update_progress)[0]
        progress.finish()
        super(RemoteArchiveTableList, self).load(path)
