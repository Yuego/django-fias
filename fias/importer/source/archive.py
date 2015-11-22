#coding: utf-8
from __future__ import unicode_literals, absolute_import

import datetime
import rarfile
from progress.bar import Bar

try:
    from urllib.request import urlretrieve
    from urllib.error import HTTPError
except ImportError:
    from urllib import urlretrieve
    HTTPError = IOError

from .tablelist import TableList, TableListLoadingError

rarfile.UNRAR_TOOL = 'unrar'


class BadArchiveError(TableListLoadingError):
    pass


class LocalArchiveTableList(TableList):

    def __init__(self, src, version=None):
        self._archive = None
        super(LocalArchiveTableList, self).__init__(src=src, version=version)

    def load_archive(self):
        try:
            self._archive = rarfile.RarFile(self._src)
        except (rarfile.NotRarFile, rarfile.BadRarFile) as e:
            raise BadArchiveError('Archive: `{0}`, ver: `{1}` corrupted'
                                  ' or is not rar-archive'.format(self._src))

        if not self._archive.namelist():
            raise BadArchiveError('Archive: `{0}`, ver: `{1}` is empty'
                                  ''.format(self._src))

    @property
    def source(self):
        if self._archive is None:
            self.load_archive()
        return self._archive

    def get_tables_list(self):
        return self.source.namelist()

    def get_date_info(self, name):
        info = self.source.getinfo(name)
        return datetime.date(*info.date_time[0:3])

    def open(self, filename):
        return self.source.open(filename)


class DlProgressBar(Bar):
    message = 'Downloading: '
    suffix = '%(index)d/%(max)d'
    hide_cursor = False


class RemoteArchiveTableList(LocalArchiveTableList):

    def __init__(self, src, version=None):
        self._url = src
        super(RemoteArchiveTableList, self).__init__(src=src, version=version)

    def load_archive(self):
        progress = DlProgressBar()

        def update_progress(count, block_size, total_size):
            progress.goto(int(count * block_size * 100 / total_size))

        try:
            self._src = urlretrieve(self._url, reporthook=update_progress)[0]
        except HTTPError as e:
            raise BadArchiveError('Can not download data archive at url `{0}`. Error occured: "{1}"'.format(
                self._url, str(e)
            ))
        progress.finish()

        super(RemoteArchiveTableList, self).load_archive()
