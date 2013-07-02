#coding: utf-8
from __future__ import unicode_literals, absolute_import

from urllib import urlretrieve, urlcleanup
from xml.parsers import expat
import datetime
import rarfile
import warnings

from fias.models import *
from fias.config import FIAS_TABLES


class FiasFiles(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(FiasFiles, cls).__new__(cls)

            self = cls.instance

            self.fias_list = {}

            self.archives = {}
            self._full_version = None

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

    def _get_full_archive(self):
        if 'full' not in self.archives:
            self._retrieve_full_archive()
        return self.archives['full']

    def _set_full_archive(self, value):
        if value is not None:
            self.archives['full'] = value
            self._full_version = None

    full_archive = property(fset=_set_full_archive, fget=_get_full_archive)

    def _retrieve_full_archive(self):
        if 'full' not in self.archives:
            self._full_version = self.latest
            self.archives['full'] = urlretrieve(self.fias_list[self._full_version.ver]['FiasCompleteXmlUrl'])

    def _retrieve_update_archive(self, version):
        if version.ver not in self.archives:
            self.archives[version.ver] = urlretrieve(self.fias_list[version.ver]['FiasDeltaXmlUrl'])[0]

    def _walk(self, ver=None):
        if ver is not None:
            self._retrieve_update_archive(ver)
            f = self.archives[ver.ver]
        else:
            self._retrieve_full_archive()
            f = self.archives['full']

        self._arch = rarfile.RarFile(f)

        for filename in self._arch.namelist():
            tablename = filename.split("_")[-3].lower()
            dump_date = datetime.datetime.strptime(filename.split("_")[-2], "%Y%m%d").date()

            if ver is None:
                try:
                    ver = Version.objects.filter(dumpdate=dump_date).latest('dumpdate')
                except Version.DoesNotExist:
                    ver = Version.objects.filter(dumpdate__lte=dump_date).latest('dumpdate')

            yield (tablename, dump_date, ver, filename)

    def get_tablelist(self, ver=None):
        flist = {}
        for (table, fdate, fver, filename) in self._walk(ver):
            flist[table] = {
                'date': fdate,
                'ver': fver,
                'file': filename
            }
        return flist.copy()

    def open(self, filename):
        return self._arch.open(filename)

    def __del__(self):
        urlcleanup()


class BulkCreate(object):

    def __init__(self, model, pk, upd_field=None):
        self.model = model
        self.pk = pk
        self.upd_field = upd_field

        self.objects = []
        self.counter = 0
        self.upd_counter = 0

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
            self.counter += 1
        elif self.upd_field is not None and self.upd_field in data:
            old_obj = self.model.objects.get(**{self.pk: key})
            if getattr(old_obj, self.upd_field) < data[self.upd_field]:
                for k, v in data:
                    setattr(old_obj, k, v)
                old_obj.save()
                self.upd_counter += 1

            del old_obj
        del data

        if self.counter and self.counter % 10000 == 0:
            self._create()
            print 'Created {0} objects'.format(self.counter)

    def finish(self):
        if self.objects:
            self._create()

        if self.upd_counter:
            print 'Updated {0} objects'.format(self.upd_counter)

    def __del__(self):
        del self.model
        del self.pk
        del self.objects
        del self.counter
        del self.upd_counter


_socrbase_bulk = BulkCreate(SocrBase, 'kod_t_st')


def _socrbase_row(name, attrib):
    if name == 'AddressObjectType':
        _socrbase_bulk.push(attrib)


_normdoc_bulk = BulkCreate(NormDoc, 'normdocid')


def _normdoc_row(name, attrib):
    if name == 'NormativeDocument':
        _normdoc_bulk.push(attrib)


_addr_obj_bulk = BulkCreate(AddrObj, 'aoguid', 'updatedate')


def _addrobj_row(name, attrib):
    if name == 'Object':

        if attrib.get('LIVESTATUS', '0') != '1':
            return

        end_date = datetime.datetime.strptime(attrib.pop('ENDDATE'), "%Y-%m-%d").date()
        if end_date < datetime.date.today():
            return

        start_date = datetime.datetime.strptime(attrib.pop('STARTDATE'), "%Y-%m-%d").date()
        if start_date > datetime.date.today():
            print 'Date in future - skipping...'
            print attrib
            return

        attrib['ENDDATE'] = end_date
        attrib['STARTDATE'] = start_date

        _addr_obj_bulk.push(attrib)


_house_bulk = BulkCreate(House, 'houseguid', 'updatedate')


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

    print 'Processing table `{0}`...'.format(table)

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

    print 'Processing table `{0}` is finished'.format(table)


def fill_database(f):
    fias = FiasFiles()
    fias.full_archive = f
    tables = fias.get_tablelist()
    for table in FIAS_TABLES:
        table_info = tables.get(table, None)
        if table_info is not None:
            try:
                status = Status.objects.get(table=table)
            except Status.DoesNotExist:
                f = fias.open(table_info['file'])

                _process_table(table, f)


                status = Status(table=table, ver=table_info['ver'])
                status.save()
            else:
                print (('Table `{0}` has version `{1}`. '
                        'Please use --force for replace '
                        'all tables. Skipping...'.format(status.table, status.ver)))


def update_database():
    fias = FiasFiles()
    tables = fias.get_tablelist(fias.latest)
    for table in FIAS_TABLES:
        table_info = tables.get(table, None)
        if table_info is not None:
            try:
                status = Status.objects.get(table=table)
            except Status.DoesNotExist:
                warnings.warn('Can`t update table `{0}`. Status is unknown!'.format(table))
            else:
                if status.ver.ver < fias.latest.ver:
                    f = fias.open(table_info['file'])

                    _process_table(table, f, True)

                    status.ver = fias.latest
                    status.save()
                else:
                    print ('Table `{0}` is up to date. Version: {1}'.format(status.table, status.ver))