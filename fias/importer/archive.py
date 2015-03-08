#coding: utf-8
from __future__ import unicode_literals, absolute_import

from fias.config import FIAS_TABLES, FIAS_DELETED_TABLES

from fias.importer.loader import loader
from fias.importer.log import log
from fias.importer.table import Table
from fias.models import Status, Version
from lxml.etree import XMLSyntaxError
import rarfile
try:
    from urllib import urlretrieve
except ImportError:
    from urllib.request import urlretrieve


class BadArchiveError(Exception):
    pass


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

        if self._version is None:
            self._version = self._get_version()

        return self._archive

    @property
    def tables(self):
        if self._tables is None:
            self._tables = {}
            for filename in self._archive.namelist():
                table = Table(archive=self, filename=filename)
                self._tables[table.full_name] = table
        
        return self._tables

    @property
    def dump_date(self):
        if self._date is None:
            table = self.tables.items()[0][1]
            self._date = table.date
        return self._date

    def _get_version(self):
        try:
            return Version.objects.filter(dumpdate=self.dump_date).latest('dumpdate')
        except Version.DoesNotExist:
            return Version.objects.filter(dumpdate__lte=self.dump_date).latest('dumpdate')

    def open(self, filename):
        return self._archive.open(filename)

    def load(self, truncate=False, skip=False):
        for table_name in FIAS_TABLES:
            try:
                table = self.tables[table_name]
            except KeyError:
                log.debug('Table `{0}` not found in archive'.format(table_name))
                continue

            try:
                status = Status.objects.get(table=table_name)
            except Status.DoesNotExist:

                log.info('Filling table `{0}` to ver. {1}...'.format(table.full_name, self._version.ver))

                ldr = loader(table)
                ldr.load(truncate=truncate, update=False)

                status = Status(table=table.full_name, ver=self._version)
                status.save()

                self._process_deleted_table(table_name)
            else:
                log.warning('Table `{0}` has version `{1}`. '
                            'Please use --force-replace for replace '
                            'all tables. Skipping...'.format(status.table, status.ver))

    def _process_deleted_table(self, table_name):
        if table_name in FIAS_DELETED_TABLES:
            try:
                table = self.tables['del_' + table_name]
            except KeyError:
                return

            #TODO: дописать обработчик


class DeltaArchive(Archive):
    field_name = 'delta_xml_url'

    def load(self, truncate=False, skip=False):
        to_update = [s.table for s in Status.objects.filter(ver__ver__lt=self._version.ver)]
        for table_name in set(to_update) & set(FIAS_TABLES):
            try:
                table = self.tables[table_name]
            except KeyError:
                log.debug('Table `{0}` not found in archive'.format(table_name))
                continue

            status = Status.objects.get(table=table.full_name)

            log.info('Updating table `{0}` from {1} to {2}...'.format(table.full_name,
                                                                      status.ver.ver,
                                                                      self._version.ver))

            ldr = loader(table)
            try:
                ldr.load(truncate=False, update=True)
            except XMLSyntaxError as e:
                msg = 'XML file for table `{0}` is broken. Data not loaded!'.format(table.full_name)
                if skip:
                    log.error(msg)
                else:
                    raise BadArchiveError(msg)
            else:
                status.ver = self._version
                status.save()

            self._process_deleted_table(table_name)
