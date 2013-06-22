#coding: utf-8
from __future__ import unicode_literals, absolute_import

from urllib import urlretrieve, urlcleanup
from xml.parsers import expat
import datetime
import os
import rarfile
import warnings

from django_fias.models import *
from django_fias.config import FIAS_TABLES


class FiasFiles(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(FiasFiles, cls).__new__(cls)

            self = cls.instance

            self.fias_list = {}

            self.archive = None
            self.arch_ver = None
            self.updates = {}

            self._latest = None
            self._arch = None

            from pysimplesoap import client
            client.TIMEOUT = None
            fias = client.SoapClient(wsdl="http://fias.nalog.ru/WebServices/Public/DownloadService.asmx?WSDL", trace=False)
            fias_list_raw = fias.GetAllDownloadFileInfo()
            if fias_list_raw and 'GetAllDownloadFileInfoResult' in fias_list_raw:
                for it in fias_list_raw['GetAllDownloadFileInfoResult']:
                    one = it['DownloadFileInfo']
                    try:
                        ver = Version.objects.get(ver=one['VersionId'])
                    except Version.DoesNotExist:
                        ver = Version(**{
                            'ver': one['VersionId'],
                            'dumpdate': datetime.datetime.strptime(one['TextVersion'][-10:], "%d.%m.%Y").date(),
                        })
                        ver.save()

                    del one['VersionId']
                    self.fias_list[ver.ver] = one

        return cls.instance

    @property
    def latest(self):
        if self._latest is None:
            self._latest = Version.objects.latest('dumpdate')

        return self._latest

    def _retrieve_full_archive(self):
        self.arch_ver = self.latest
        self.archive = urlretrieve(self.fias_list[self.arch_ver.ver]['FiasCompleteXmlUrl'])

    def _walk(self, f, version=None):
        self._arch = rarfile.RarFile(f)

        for filename in self._arch.namelist():
            tablename = filename.split("_")[-3].lower()
            dump_date = datetime.datetime.strptime(filename.split("_")[-2], "%Y%m%d").date()

            if version is None:
                try:
                    version = Version.objects.filter(dumpdate=dump_date).latest('dumpdate')
                except Version.DoesNotExist:
                    version = Version.objects.filter(dumpdate__lte=dump_date).latest('dumpdate')

            yield (tablename, dump_date, version, filename)

    def walk_full(self, archive=None):
        if archive is not None:
                if os.path.exists(archive):
                    self.archive = archive
                else:
                    raise IOError('File `{0}` does not exist!'.format(archive))
        else:
            self._retrieve_full_archive()

        return self._walk(self.archive)

    def walk_update(self, version):
        if version.ver not in self.updates:
            self.updates[version.ver] = urlretrieve(self.fias_list[version.ver]['FiasDeltaXmlUrl'])[0]
        archfile = self.updates[version.ver]

        return self._walk(archfile, version)

    def open(self, filename):
        return self._arch.open(filename)

    def __del__(self):
        urlcleanup()


class BulkCreate(object):

    def __init__(self, model, pk):
        self.model = model
        self.pk = pk

        self.objects = []
        self.counter = 0

    def _lower_keys(self, d):
        return dict((k.lower(), v) for k, v in d.iteritems())

    def _create(self):
        self.model.objects.bulk_create(self.objects)
        del self.objects
        self.objects = []

    def push(self, data):
        data = self._lower_keys(data)

        key = data[self.pk]

        if not self.model.objects.filter(**{self.pk: key}).exists():
            self.objects.append(self.model(**data))
            del data
            self.counter += 1

        if self.counter and self.counter % 25000 == 0:
            self._create()
            print 'Created {0} objects'.format(self.counter)

    def finish(self):
        if self.objects:
            self._create()

    def __del__(self):
        del self.model
        del self.pk
        del self.objects
        del self.counter


_socrbase_bulk = BulkCreate(SocrBase, 'kod_t_st')


def _socrbase_row(name, attrib):
    if name == 'AddressObjectType':
        _socrbase_bulk.push(attrib)


_normdoc_bulk = BulkCreate(NormDoc, 'normdocid')


def _normdoc_row(name, attrib):
    if name == 'NormativeDocument':
        _normdoc_bulk.push(attrib)


_addr_obj_bulk = BulkCreate(AddrObj, 'aoid')


def _addrobj_row(name, attrib):
    if name == 'Object':

        if attrib.get('LIVESTATUS', '0') != '1':
            return

        end_date = datetime.datetime.strptime(attrib.pop('ENDDATE'), "%Y-%m-%d").date()
        if end_date < datetime.date.today():
            return

        if 'NORMDOC' in attrib:
            docid = attrib.pop('NORMDOC')
            try:
                doc = NormDoc.objects.get(normdocid=docid)
            except NormDoc.DoesNotExist:
                print 'Doc', docid, 'does not exist. Skipping'
            else:
                attrib['NORMDOC'] = doc

        start_date = datetime.datetime.strptime(attrib.pop('STARTDATE'), "%Y-%m-%d").date()
        if start_date > datetime.date.today():
            print 'Date in future - skipping...'
            print attrib
            return

        attrib['ENDDATE'] = end_date
        attrib['STARTDATE'] = start_date

        _addr_obj_bulk.push(attrib)


_house_bulk = BulkCreate(House, 'houseguid')


def _house_row(name, attrib):
    if name == 'House':
        #TODO: реализовать
        return


def _process_table(table, f, update=False):
    if f is None:
        print 'Omg! Where`s my file???'
        return

    if table not in FIAS_TABLES:
        print 'Impossible... but... Skipping table `{0}`'.format(table)
        return

    p = expat.ParserCreate()
    bulk = None

    if table == 'socrbase':
        if not update:
            SocrBase.objects.all().delete()

        p.StartElementHandler = _socrbase_row
        bulk = _socrbase_bulk

    elif table == 'normdoc':
        if not update:
            NormDoc.objects.all().delete()

        p.StartElementHandler = _normdoc_row
        bulk = _normdoc_bulk
    elif table == 'addrobj':
        if not update:
            AddrObj.objects.all().delete()

        p.StartElementHandler = _addrobj_row
        bulk = _addr_obj_bulk
    elif table == 'house':
        if not update:
            House.objects.all().delete()

        p.StartElementHandler = _house_row
        bulk = _house_bulk
        #TODO: убрать как только будет реализовано до конца (см. выше)
        return
    else:
        return

    p.ParseFile(f)
    bulk.finish()
    del p
    del f
    del bulk

    print 'Processing of table `{0}` is finished'.format(table)


def fill_database(f):
    fias = FiasFiles()
    for (table, fdate, fver, filename) in fias.walk_full(f):
        if table in FIAS_TABLES:
            try:
                status = Status.objects.get(table=table)
            except Status.DoesNotExist:
                f = fias.open(filename)

                _process_table(table, f)


                status = Status(table=table, ver=fver)
                status.save()
            else:
                print (('Table `{0}` has version `{1}`. '
                        'Please use --force for replace '
                        'all tables. Skipping...'.format(status.table, status.ver)))


def update_database():
    fias = FiasFiles()
    for (table, fdate, fver, filename) in fias.walk_update(fias.latest):
        if table in FIAS_TABLES:
            try:
                status = Status.objects.get(table=table)
            except Status.DoesNotExist:
                warnings.warn('Can`t update table `{0}`. Status is unknown!'.format(table))
            else:
                if status.ver.ver < fias.latest.ver:
                    f = fias.open(filename)

                    _process_table(table, f, True)

                    status.ver = fias.latest
                    status.save()
                else:
                    print ('Table `{0}` is up to date. Version: {1}'.format(status.table, status.ver))