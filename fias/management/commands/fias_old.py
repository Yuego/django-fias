#coding: utf-8
from __future__ import unicode_literals, absolute_import

import sys
from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.translation import activate

from fias.importer.commands import load_complete_xml, load_delta_xml
from fias.importer.version import fetch_version_info
from fias.management.utils.weights import rewrite_weights
from fias.models import Status



class Command(BaseCommand):
    help = 'Fill or update FIAS database'
    usage_str = 'Usage: ./manage.py fias [--file <filename>|--remote-file]'\
                ' [--force-replace] [--really-replace] [--update [--skip]]'\
                ' [--fill-weights]'

    option_list = BaseCommand.option_list + (
        make_option('--file', action='store', dest='file', default=None,
                    help='Load file into DB'),
        make_option('--remote-file', action='store_true', dest='remote', default=False,
                    help='Download full archive and load it into DB'),
        make_option('--force-replace', action='store_true', dest='force', default=False,
                    help='Force replace database'),
        make_option('--really-replace', action='store_true', dest='really', default=False,
                    help='If data exist in any table, you should confirm their removal and replacement'
                         ', as this may result in the removal of related data from other tables!'),
        make_option('--update', action='store_true', dest='update', default=False,
                    help='Fetch `ver` and load into db'),
        make_option('--fill-weights', action='store_true', dest='weights', default=False,
                    help='Fill default weights'),
        make_option('--skip', action='store_true', dest='skip', default=False,
                    help='Skip the bad delta files when upgrading'),
    )

    def handle(self, *args, **options):
        remote = options.pop('remote')
        force = options.pop('force')
        really = options.pop('really')
        update = options.pop('update')
        skip = options.pop('skip')
        weights = options.pop('weights')

        path = options.pop('file') if not remote else None

        if path is None and not remote and not update and not weights:
            self.error(self.usage_str)

        if (path or remote) and Status.objects.count() > 0 and not really:
            self.error('One of the tables contains data. Truncate all FIAS tables manually '
                       'or enter key --really-replace, to clear the table by means of Django ORM')

        truncate = False
        fetch_version_info(update_all=True)

        # Force Russian language for internationalized projects
        if settings.USE_I18N:
            activate('ru')

        if path or remote:
            if force:
                truncate = True
                Status.objects.all().delete()
            load_complete_xml(path=path, truncate=truncate)

        if update:
            print ('Database updating...')
            load_delta_xml(skip=skip)

        if weights:
            print ('Rewriting weights')
            rewrite_weights()

    def error(self, message, code=1):
        print(message)
        sys.exit(code)
