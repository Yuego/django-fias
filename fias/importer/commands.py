#coding: utf-8
from __future__ import unicode_literals, absolute_import

import os
from django.db.models import Min
from fias.config import TABLES
from fias.importer.source import *
from fias.importer.table import BadTableError
from fias.importer.loader import TableLoader, TableUpdater
from fias.importer.log import log
from fias.models import Status, Version


def get_tablelist(path, data_format):
    if path is None:
        latest_version = Version.objects.latest('dumpdate')
        url = getattr(latest_version, 'complete_{0}_url'.format(data_format))

        tablelist = RemoteArchiveTableList(src=url, version=latest_version)

    else:
        if os.path.isfile(path):
            tablelist = LocalArchiveTableList(src=path)

        elif os.path.isdir(path):
            tablelist = DirectoryTableList(src=path)

        elif path.startswith('http://') or path.startswith('https://') or path.startswith('//'):
            tablelist = RemoteArchiveTableList(src=path)

        else:
            raise TableListLoadingError('Path `{0}` is not valid table list source')

    return tablelist


def get_table_names(tables):
    return tables if tables is not None else TABLES


def load_complete_data(path=None,
                       data_format='xml',
                       truncate=False, raw=False,
                       limit=10000, tables=None):

    tablelist = get_tablelist(path=path, data_format=data_format)
    clear = {}

    for tbl in get_table_names(tables):
        clear[tbl] = truncate

        try:
            st = Status.objects.get(table=tbl)
            if clear[tbl]:  # Удаляем запись из БД и вызываем-таки исключение сами %)
                st.delete()
                raise Status.DoesNotExist()
        except Status.DoesNotExist:
            for table in tablelist.tables[tbl]:
                if clear[tbl]:
                    table.truncate()
                    # Может быть несколько файлов для одной таблицы
                    # Не надо очищать таблицу перед загрузкой каждого
                    clear[tbl] = False

                loader = TableLoader(limit=limit)
                loader.load(tablelist=tablelist, table=table)

            st = Status(table=tbl, ver=tablelist.version)
            st.save()
        else:
            log.warning('Table `{0}` has version `{1}`. '
                        'Please use --truncate for replace '
                        'all table contents. Skipping...'.format(st.table, st.ver))


def update_data(path=None, skip=False, data_format='xml', limit=1000, tables=None):
    tablelist = get_tablelist(path=path, data_format=data_format)

    for tbl in get_table_names(tables):
        st = Status.objects.get(table=tbl)

        log.info('Updating table `{0}` from {1} to {2}...'.format(tbl,
                                                                  st.ver.ver,
                                                                  tablelist.version))

        for table in tablelist.tables[tbl]:
            loader = TableUpdater(limit=limit)
            try:
                loader.load(tablelist=tablelist, table=table)
            except BadTableError as e:
                if skip:
                    log.error(str(e))
                else:
                    raise

        st.ver = tablelist.version
        st.save()


def auto_update_data(skip=False, data_format='xml', limit=1000):
    min_version = Status.objects.filter(table__in=get_table_names(None)).aggregate(Min('ver'))['ver__min']

    if min_version is not None:
        for version in Version.objects.filter(ver__gt=min_version).order_by('ver'):
            url = getattr(version, 'delta_{0}_url'.format(data_format))
            update_data(path=url, skip=skip, data_format=data_format, limit=limit)
    else:
        raise TableListLoadingError('Not available. Please import the data before updating')
