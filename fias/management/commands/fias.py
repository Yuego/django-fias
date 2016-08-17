# coding: utf-8
from __future__ import unicode_literals, absolute_import

import sys
from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.translation import activate

from fias.config import TABLES
from fias.importer.source import TableListLoadingError
from fias.importer.commands import auto_update_data, load_complete_data
from fias.importer.version import fetch_version_info
from fias.management.utils.weights import rewrite_weights
from fias.models import Status


class Command(BaseCommand):
    help = 'Fill or update FIAS database'
    usage_str = 'Usage: ./manage.py fias [--src <path|filename|url|AUTO> [--truncate] [--i-know-what-i-do]]'\
                ' [--update [--skip]]'\
                ' [--format <xml|dbf>] [--limit=<N>] [--tables=<{0}>]'\
                ' [--update-version-info <yes|no>]'\
                ' [--fill-weights]'.format(','.join(TABLES))

    option_list = BaseCommand.option_list + (
        make_option('--src', action='store', dest='src', default=None,
                    help='Load dir|file|url into DB. If not specified, the source is automatically selected'),

        make_option('--truncate', action='store_true', dest='truncate', default=False,
                    help='Truncate tables before loading data'),
        make_option('--i-know-what-i-do', action='store_true', dest='doit', default=False,
                    help='If data exist in any table, you should confirm their removal and replacement'
                         ', as this may result in the removal of related data from other tables!'),

        make_option('--update', action='store_true', dest='update', default=False,
                    help='Update database from http://fias.nalog.ru'),
        make_option('--skip', action='store_true', dest='skip', default=False,
                    help='Skip the bad delta files when upgrading'),


        make_option('--format', action='store', dest='format',
                    type='choice', choices=['xml', 'dbf'], default='xml',
                    help='Preferred source data format. Possible choices: xml|dbf'),

        make_option('--limit', action='store', dest='limit',
                    type='int', default=10000,
                    help='Limit rows for bulk operations. Default value: 10000'),

        make_option('--tables', action='store', dest='tables', default=None,
                    help='Comma-separated list of tables to import'),

        make_option('--update-version-info', action='store', dest='update-version-info',
                    type='choice', choices=['yes', 'no'], default='yes',
                    help='Update list of available database versions from http://fias.nalog.ru'),

        make_option('--fill-weights', action='store_true', dest='weights', default=False,
                    help='Fill default weights'),

    )

    def handle(self, *args, **options):
        from fias.importer.timer import Timer
        Timer.init()

        src = options.pop('src')
        remote = False
        if src and src.lower() == 'auto':
            src = None
            remote = True

        truncate = options.pop('truncate')
        doit = options.pop('doit')

        update = options.pop('update')
        skip = options.pop('skip')

        weights = options.pop('weights')

        if not any([src, remote, update, weights]):
            self.error(self.usage_str)

        if (src or remote) and Status.objects.count() > 0 and not doit:
            self.error('One of the tables contains data. Truncate all FIAS tables manually '
                       'or enter key --i-know-what-i-do, to clear the table by means of Django ORM')

        fetch = options.pop('update-version-info')
        if fetch == 'yes':
            fetch_version_info(update_all=True)

        # Force Russian language for internationalized projects
        if settings.USE_I18N:
            activate('ru')

        fmt = options.pop('format')
        limit = int(options.pop('limit'))
        tables = options.pop('tables')
        tables = set(tables.split(',')) if tables else set()

        if not tables.issubset(set(TABLES)):
            diff = ', '.join(tables.difference(TABLES))
            self.error('Tables `{0}` are not listed in the FIAS_TABLES and can not be processed'.format(diff))

        if src or remote:

            try:
                load_complete_data(path=src, data_format=fmt, truncate=truncate, limit=limit)
            except TableListLoadingError as e:
                self.error(str(e))

        if update:

            try:
                auto_update_data(skip=skip, data_format=fmt, limit=limit)
            except TableListLoadingError as e:
                self.error(str(e))

        if weights:
            rewrite_weights()

    def error(self, message, code=1):
        print(message)
        sys.exit(code)
