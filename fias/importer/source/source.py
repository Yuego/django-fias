#coding: utf-8
from __future__ import unicode_literals, absolute_import

import datetime

from fias.importer.log import log
from fias.importer.table import Table
from fias.models import Status, Version









class Archive(object):
    field_name = 'complete_xml_url'

    def __init__(self, version=None, path=None):
        assert version is not None or path is not None, 'You must specify version or path to archive'
        if version is not None:
            assert isinstance(version, Version), '`{0}` is not {1}'.format(repr(version), type(Version))

        self._version = version
        self._tables = None
        self._path = path
        self._archive = None
        self._date = None
        self._retrieve(version, path)

    def _retrieve(self, version=None, path=None):
        self._path = path
        if self._path is None:
            path = getattr(version, self.field_name)
            log.info('Downloading file: {0}'.format(path))
            self._path = urlretrieve(path)[0]

        try:
            self._archive = rarfile.RarFile(self._path)
        except (rarfile.NotRarFile, rarfile.BadRarFile) as e:
            raise BadArchiveError('Archive: `{0}`, ver: `{1}` corrupted'
                                  ' or is not rar-archive'.format(path, version or 'unknown'))

        if not self._archive.namelist():
            raise BadArchiveError('Archive: `{0}`, ver: `{1}` is empty'
                                  ''.format(path, version or 'unknown'))

        if self._version is None:
            self._version = self._get_version()

        return self._archive

    @property
    def tables(self):
        if not hasattr(self, '_tables'):
            self._tables = self._archive.namelist()

        if self._tables is None:
            self._tables = {}
            for filename in self._archive.namelist():
                table = TableFactory.parse(filename=filename)
                self._tables.setdefault(table.name, []).append(table)

        return self._tables

    @property
    def dump_date(self):
        if self._date is None:
            first_name = self._archive.namelist()[0]
            info = self._archive.getinfo(first_name)
            self._date = datetime.date(*info.date_time[0:3])

        return self._date

    def _get_version(self):
        try:
            return Version.objects.filter(dumpdate=self.dump_date).latest('dumpdate')
        except Version.DoesNotExist:
            return Version.objects.filter(dumpdate__lte=self.dump_date).latest('dumpdate')

    def open(self, filename):
        return self._archive.open(filename)
