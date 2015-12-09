# coding: utf-8
from __future__ import unicode_literals, absolute_import

import sys
from optparse import make_option

from django.core.management.base import BaseCommand

from fias.config import TABLES
from fias.importer.commands import get_tablelist


class Command(BaseCommand):
    help = 'Утилита для поиска дубликатов по первичному ключу'
    usage_str = 'Usage: ./manage.py --key <pk> --src <path> --table <table>'

    option_list = BaseCommand.option_list + (
        make_option('--key', action='store', dest='pk',
                    help='List duplicates by PK'),

        make_option('--src', action='store', dest='src',
                    help='Source directory for duplicates search'),

        make_option('--table', action='store', dest='table', type='choice', choices=TABLES,
                    help='Table to search for duplicates'),


    )

    def handle(self, *args, **options):
        key = options.pop('pk')
        src = options.pop('src')
        table = options.pop('table')

        if not any([key, src, table]):
            self.error(self.usage_str)

        tablelist = get_tablelist(path=src, data_format='xml')
        for tbl in tablelist.tables[table]:

            for item in tbl.rows(tablelist=tablelist):
                if item.pk == key:
                    print(item)
                    print(item.__dict__)

    def error(self, message, code=1):
        print(message)
        sys.exit(code)
