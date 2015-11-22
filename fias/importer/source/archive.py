#coding: utf-8
from __future__ import unicode_literals, absolute_import

import datetime
import os
import rarfile
import shutil
import tempfile
from progress.bar import Bar

try:
    from urllib.request import urlretrieve
    from urllib.error import HTTPError
except ImportError:
    from urllib import urlretrieve
    HTTPError = IOError

from fias.importer.table import table_dbf_re, table_dbt_re

from .tablelist import TableList, TableListLoadingError

rarfile.UNRAR_TOOL = 'unrar'


class BadArchiveError(TableListLoadingError):
    pass


class LocalArchiveTableList(TableList):

    def __init__(self, src, version=None):
        self._archive = None

        self._unpack = False
        self._list = None
        self._path = None
        super(LocalArchiveTableList, self).__init__(src=src, version=version)

    def unpack(self):
        self._path = tempfile.mkdtemp()

        self._archive.extractall(self._path)

    def load_archive(self):
        try:
            self._archive = rarfile.RarFile(self._src)
        except (rarfile.NotRarFile, rarfile.BadRarFile) as e:
            raise BadArchiveError('Archive: `{0}`, ver: `{1}` corrupted'
                                  ' or is not rar-archive'.format(self._src))

        if not self._archive.namelist():
            raise BadArchiveError('Archive: `{0}`, ver: `{1}` is empty'
                                  ''.format(self._src))

        first_name = self._archive.namelist()[0]
        if table_dbf_re.match(first_name) or table_dbt_re.match(first_name):
            self._unpack = True
            self.unpack()


    @property
    def source(self):
        if self._archive is None:
            self.load_archive()

        if not self._unpack:
            return self._archive
        else:
            return self._path

    def get_tables_list(self):
        if self._archive is None:
            self.load_archive()

        if not self._unpack:
            return self.source.namelist()
        else:
            if self._list is None:
                self._list = [f for f in os.listdir(self.source) if os.path.isfile(os.path.join(self.source, f))]
            return self._list

    def get_date_info(self, name):
        if not self._unpack:
            info = self.source.getinfo(name)
            return datetime.date(*info.date_time[0:3])
        else:
            st = os.stat(os.path.join(self.source, name))
            return datetime.datetime.fromtimestamp(st.st_mtime)

    def get_full_path(self, filename):
        return os.path.join(self.source, filename)

    def open(self, filename):
        if not self._unpack:
            return self.source.open(filename)
        else:
            return self.get_full_path(filename)

    def __del__(self):
        if self._unpack:
            shutil.rmtree(self._path, ignore_errors=True)


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
