#coding: utf-8
from __future__ import unicode_literals, absolute_import

import os
import sys
from optparse import make_option

from django.core.management.base import BaseCommand

from fias.management.utils.sphinx import render_sphinx_config


class Command(BaseCommand):
    help = 'Configure Sphinx engine'
    usage_str = 'Usage: ./manage.py fias_sphinx --path=PATH [--full]'

    option_list = BaseCommand.option_list + (
        make_option('--path', action='store', dest='path',
            help='Path to sphinx index'),
        make_option('--full', action='store_true', dest='full', default=False,
            help='Generate full sphinx config'),
    )

    def handle(self, *args, **options):
        path = options.pop('path')

        if not path:
            self.error(self.usage_str)

        path = os.path.abspath(path)

        full = options.pop('full')

        print ('\n'.join(render_sphinx_config(path, full)))

    def error(self, message, code=1):
        print(message)
        sys.exit(code)