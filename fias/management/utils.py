#coding: utf-8
from __future__ import unicode_literals, absolute_import

from urllib import urlretrieve, urlcleanup
from lxml import etree
import datetime
import rarfile
import warnings

from django import db
from django.conf import settings
from django.db.models import Min

from fias.models import *
from fias.config import FIAS_TABLES, FIAS_DELETED_TABLES

_today = datetime.date.today()


def _fast_iter(context, func):
    for event, elem in context:
        func(elem)
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]
    del context


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

            from suds.client import Client
            client = Client(url="http://fias.nalog.ru/WebServices/Public/DownloadService.asmx?WSDL")
            result = client.service.GetAllDownloadFileInfo()
            for it in result.DownloadFileInfo:
                try:
                    ver = Version.objects.get(ver=it['VersionId'])
                except Version.DoesNotExist:
                    ver = Version(**{
                        'ver': it['VersionId'],
                        'dumpdate': datetime.datetime.strptime(it['TextVersion'][-10:], "%d.%m.%Y").date(),
                    })
                    ver.save()

                self.fias_list[ver.ver] = it

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
            _prefix, _date = filename.lower().rsplit('_', 2)[0:2]

            tablename = _prefix.replace('as_', '')
            dump_date = datetime.datetime.strptime(_date, "%Y%m%d").date()

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
        #print flist
        return flist.copy()

    def open(self, filename):
        return self._arch.open(filename)

    def __del__(self):
        urlcleanup()


class BulkCreate(object):

    def __init__(self, model, pk, upd_field=None, mode='update'):
        self._mode = 'update'

        self.model = model
        self.pk = pk
        self.upd_field = upd_field
        self._set_mode(mode)

        self.objects = []
        self.counter = 0
        self.upd_counter = 0
        
    def _set_mode(self, value):
        assert value in ('fill', 'update'), 'Wrong mode `{}`'.format(value)
        self._mode = value

    def _get_mode(self):
        return self._mode

    mode = property(fset=_set_mode, fget=_get_mode)

    def reset_counters(self):
        self.upd_counter = 0
        self.counter = 0

    def _lower_keys(self, d):
        return dict((k.lower(), v) for k, v in d.iteritems())

    def _create(self):
        self.model.objects.bulk_create(self.objects)
        self.objects = []
        if settings.DEBUG:
            db.reset_queries()

    def push(self, raw_data, related_attrs=None):
        data = self._lower_keys(raw_data.attrib)

        if isinstance(related_attrs, dict):
            data.update(related_attrs)

        key = data[self.pk]

        if self.mode == 'fill' or not self.model.objects.filter(**{self.pk: key}).exists():
            self.objects.append(self.model(**data))
            self.counter += 1
        elif self.upd_field is not None and self.upd_field in data:
            old_obj = self.model.objects.get(**{self.pk: key})
            data[self.upd_field] = datetime.datetime.strptime(data[self.upd_field], "%Y-%m-%d").date()

            if getattr(old_obj, self.upd_field) < data[self.upd_field]:
                for k, v in data.items():
                    setattr(old_obj, k, v)
                old_obj.save()
                self.upd_counter += 1

        del data

        if self.counter and self.counter % 10000 == 0:
            self._create()
            print ('Created {0} objects'.format(self.counter))

    def finish(self):
        if self.objects:
            self._create()

        if self.upd_counter:
            print ('Updated {0} objects'.format(self.upd_counter))


_socrbase_bulk = BulkCreate(SocrBase, 'kod_t_st')


def _socrbase_row(elem):
    if elem.tag == 'AddressObjectType':
        _socrbase_bulk.push(elem)


_normdoc_bulk = BulkCreate(NormDoc, 'normdocid')


def _normdoc_row(elem):
    if elem.tag == 'NormativeDocument':
        _normdoc_bulk.push(elem)


_addr_obj_bulk = BulkCreate(AddrObj, 'aoguid', 'updatedate')


def _addrobj_row(elem):
    if elem.tag == 'Object':
        # Пропускаем изменённые объекты
        if elem.attrib.has_key('NEXTID'):
            return

        start_date = datetime.datetime.strptime(elem.attrib['STARTDATE'], "%Y-%m-%d").date()
        if start_date > _today:
            print ('Date in future - skipping...')
            return

        _addr_obj_bulk.push(elem)


_house_bulk = BulkCreate(House, 'houseguid', 'updatedate')


def _house_row(elem):
    if elem.tag == 'House':
        end_date = datetime.datetime.strptime(elem.attrib['ENDDATE'], "%Y-%m-%d").date()
        if end_date < _today:
            print ('Неактуальная запись. Пропускаем...')
            return

        start_date = datetime.datetime.strptime(elem.attrib['STARTDATE'], "%Y-%m-%d").date()
        if start_date > _today:
            print ('Date in future - skipping...')
            return

        related_attrs = dict()
        try:
            related_attrs['aoguid'] = AddrObj.objects.get(pk=elem.attrib['AOGUID'])
        except AddrObj.DoesNotExist:
            print ('AddrObj with GUID `{}` not found. Skipping house...'.format(elem.attrib['AOGUID']))
            return

        _house_bulk.push(elem, related_attrs=related_attrs)


_houseint_bulk = BulkCreate(HouseInt, 'intguid', 'updatedate')


def _houseint_row(elem):
    if elem.tag == 'HouseInterval':
        end_date = datetime.datetime.strptime(elem.attrib['ENDDATE'], "%Y-%m-%d").date()
        if end_date < _today:
            print ('Неактуальная запись. Пропускаем...')
            return

        start_date = datetime.datetime.strptime(elem.attrib['STARTDATE'], "%Y-%m-%d").date()
        if start_date > _today:
            print ('Date in future - skipping...')
            return

        related_attrs = dict()
        try:
            related_attrs['aoguid'] = AddrObj.objects.get(pk=elem.attrib['AOGUID'])
        except AddrObj.DoesNotExist:
            print ('AddrObj with GUID `{}` not found. Skipping interval...'.format(elem.attrib['AOGUID']))
            return

        _houseint_bulk.push(elem, related_attrs=related_attrs)


_landmark_bulk = BulkCreate(LandMark, 'landguid', 'updatedate')


def _landmark_row(elem):
    if elem.tag == 'Landmark':

        end_date = datetime.datetime.strptime(elem.attrib['ENDDATE'], "%Y-%m-%d").date()
        if end_date < _today:
            print ('Неактуальная запись. Пропускаем...')
            return

        start_date = datetime.datetime.strptime(elem.attrib['STARTDATE'], "%Y-%m-%d").date()
        if start_date > _today:
            print ('Date in future - skipping...')
            return

        related_attrs = dict()
        try:
            related_attrs['aoguid'] = AddrObj.objects.get(pk=elem.attrib['AOGUID'])
        except AddrObj.DoesNotExist:
            print ('AddrObj with GUID `{}` not found. Skipping landmark...'.format(elem.attrib['AOGUID']))
            return

        _landmark_bulk.push(elem, related_attrs=related_attrs)


def _process_table(table, f, ver, update=False):
    if f is None:
        print ('Omg! Where`s my file???')
        return

    if table not in FIAS_TABLES:
        print ('Impossible... but... Skipping table `{0}`'.format(table))
        return

    print ('{} table `{}` to ver. {}...'.format('Updating' if update else 'Filling', table, ver))

    serializeElementHandler = None
    bulk = None

    if table == 'socrbase':
        if not update:
            SocrBase.objects.all().delete()

        serializeElementHandler = _socrbase_row
        bulk = _socrbase_bulk

    elif table == 'normdoc':
        if not update:
            NormDoc.objects.all().delete()

        serializeElementHandler = _normdoc_row
        bulk = _normdoc_bulk
    elif table == 'addrobj':
        if not update:
            AddrObj.objects.all().delete()

        serializeElementHandler = _addrobj_row
        bulk = _addr_obj_bulk
    elif table == 'house':
        if not update:
            House.objects.all().delete()

        serializeElementHandler = _house_row
        bulk = _house_bulk

    elif table == 'houseint':
        if not update:
            HouseInt.objects.all().delete()

        serializeElementHandler = _houseint_row
        bulk = _houseint_bulk

    elif table == 'landmark':
        if not update:
            LandMark.objects.all().delete()

        serializeElementHandler = _landmark_row
        bulk = _landmark_bulk

    if bulk is None:
        return

    # Небольшая оптимизация заполнения пустых таблиц
    if not update:
        bulk.mode = 'fill'
    else:
        bulk.mode = 'update'
        bulk.reset_counters()
        
    context = etree.iterparse(f, events=('end',))

    _fast_iter(context, lambda elem: serializeElementHandler(elem))
    
    bulk.finish()

    print ('Processing table `{0}` is finished'.format(table))


#TODO: продумать алгоритм и реализовать
def _check_deleted_items(table, f, ver):
    pass


#TODO: использовать CLUSTER для PostgreSQL??? Или ну его?


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

                _process_table(table, f, table_info['ver'])

                status = Status(table=table, ver=table_info['ver'])
                status.save()

                # Check deleted items
                if table in FIAS_DELETED_TABLES:
                    table_info = tables.get('del_' + table, None)
                    if table_info is not None:
                        f = fias.open(table_info['file'])
                        _check_deleted_items(table, f, table_info['ver'])
            else:
                print (('Table `{0}` has version `{1}`. '
                        'Please use --force-replace for replace '
                        'all tables. Skipping...'.format(status.table, status.ver)))


def update_database(skip):
    fias = FiasFiles()

    min_status_ver = Status.objects.aggregate(Min('ver'))['ver__min']
    if min_status_ver is not None:
        for _version in Version.objects.filter(ver__gt=min_status_ver).order_by('ver'):

            try:
                tables = fias.get_tablelist(_version)
            except rarfile.NotRarFile:
                if skip:
                    print 'Битый архив версии {}. Пропускаем...'.format(_version)
                    continue
                else:
                    raise

            for table in FIAS_TABLES:
                try:
                    status = Status.objects.get(table=table)
                except Status.DoesNotExist:
                    warnings.warn('Can`t update table `{0}`. Status is unknown!'.format(table))
                else:
                    if status.ver.ver < _version.ver:
                        table_info = tables.get(table, None)
                        if table_info is not None:
                            f = fias.open(table_info['file'])

                            _process_table(table, f, table_info['ver'], update=True)

                            status.ver = _version
                            status.save()

                            # Check deleted items
                            if table in FIAS_DELETED_TABLES:
                                table_info = tables.get('del_' + table, None)
                                if table_info is not None:
                                    f = fias.open(table_info['file'])
                                    _check_deleted_items(table, f, table_info['ver'])
                    else:
                        print ('Table `{0}` is up to date. Version: {1}'.format(status.table, status.ver))
    else:
        print ('Not available. Please import the data before updating')