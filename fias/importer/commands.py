# coding: utf-8
from __future__ import unicode_literals, absolute_import

import os
from django.db.models import Min
from fias.config import TABLES
from fias.importer.indexes import remove_indexes_from_model, restore_indexes_for_model
from fias.importer.signals import (
    pre_drop_indexes, post_drop_indexes,
    pre_restore_indexes, post_restore_indexes,
    pre_import, post_import, pre_update, post_update
)
from fias.importer.source import *
from fias.importer.table import BadTableError
from fias.importer.loader import TableLoader, TableUpdater
from fias.importer.log import log
from fias.models import Status, Version


def get_tablelist(path, version=None, data_format='xml', tempdir=None):
    assert data_format in ['xml', 'dbf'], \
        'Unsupported data format: `{0}`. Available choices: {1}'.format(data_format, ', '.join(['xml', 'dbf']))

    if path is None:
        latest_version = Version.objects.latest('dumpdate')
        url = getattr(latest_version, 'complete_{0}_url'.format(data_format))

        tablelist = RemoteArchiveTableList(src=url, version=latest_version, tempdir=tempdir)

    else:
        if os.path.isfile(path):
            tablelist = LocalArchiveTableList(src=path, version=version, tempdir=tempdir)

        elif os.path.isdir(path):
            tablelist = DirectoryTableList(src=path, version=version, tempdir=tempdir)

        elif path.startswith('http://') or path.startswith('https://') or path.startswith('//'):
            tablelist = RemoteArchiveTableList(src=path, version=version, tempdir=tempdir)

        else:
            raise TableListLoadingError('Path `{0}` is not valid table list source'.format(path))

    return tablelist


def get_table_names(tables):
    return tables if tables else TABLES


def load_complete_data(path=None,
                       data_format='xml',
                       truncate=False,
                       limit=10000, tables=None,
                       keep_indexes=False,
                       tempdir=None,
                       ):

    tablelist = get_tablelist(path=path, data_format=data_format, tempdir=tempdir)

    pre_import.send(sender=object.__class__, version=tablelist.version)

    for tbl in get_table_names(tables):
        # Пропускаем таблицы, которых нет в архиве
        if tbl not in tablelist.tables:
            continue

        try:
            st = Status.objects.get(table=tbl)
            if truncate:
                st.delete()
                raise Status.DoesNotExist()
        except Status.DoesNotExist:
            # Берём для работы любую таблицу с именем tbl
            first_table = tablelist.tables[tbl][0]

            # Очищаем таблицу перед импортом
            if truncate:
                first_table.truncate()

            # Удаляем индексы из модели перед импортом
            if not keep_indexes:
                pre_drop_indexes.send(sender=object.__class__, table=first_table)
                remove_indexes_from_model(model=first_table.model)
                post_drop_indexes.send(sender=object.__class__, table=first_table)

            # Импортируем все таблицы модели
            for table in tablelist.tables[tbl]:
                loader = TableLoader(limit=limit)
                loader.load(tablelist=tablelist, table=table)

            # Восстанавливаем удалённые индексы
            if not keep_indexes:
                pre_restore_indexes.send(sender=object.__class__, table=first_table)
                restore_indexes_for_model(model=first_table.model)
                post_restore_indexes.send(sender=object.__class__, table=first_table)

            st = Status(table=tbl, ver=tablelist.version)
            st.save()
        else:
            log.warning('Table `{0}` has version `{1}`. '
                        'Please use --truncate for replace '
                        'all table contents. Skipping...'.format(st.table, st.ver))

    post_import.send(sender=object.__class__, version=tablelist.version)


def update_data(path=None, version=None, skip=False, data_format='xml', limit=1000, tables=None, tempdir=None):
    tablelist = get_tablelist(path=path, version=version, data_format=data_format, tempdir=tempdir)

    for tbl in get_table_names(tables):
        # Пропускаем таблицы, которых нет в архиве
        if tbl not in tablelist.tables:
            continue

        st = Status.objects.get(table=tbl)

        if st.ver.ver >= tablelist.version.ver:
            log.info('Update of the table `{0}` is not needed [{1} <= {2}]. Skipping...'.format(
                tbl, st.ver.ver, tablelist.version.ver
            ))
            continue

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


def auto_update_data(skip=False, data_format='xml', limit=1000, tables=None, tempdir=None):
    min_version = Status.objects.filter(table__in=get_table_names(None)).aggregate(Min('ver'))['ver__min']
    min_ver = Version.objects.get(ver=min_version)

    if min_version is not None:
        for version in Version.objects.filter(ver__gt=min_version).order_by('ver'):
            pre_update.send(sender=object.__class__, before=min_ver, after=version)

            url = getattr(version, 'delta_{0}_url'.format(data_format))
            update_data(
                path=url, version=version, skip=skip,
                data_format=data_format, limit=limit,
                tables=tables, tempdir=tempdir,
            )

            post_update.send(sender=object.__class__, before=min_ver, after=version)
            min_ver = version
    else:
        raise TableListLoadingError('Not available. Please import the data before updating')
