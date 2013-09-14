#coding: utf-8
from __future__ import unicode_literals, absolute_import

import sys
from optparse import make_option

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Configure Sphinx engine'
    usage_str = 'Usage: ./manage.py fias_sphinx '


    def handle(self, *args, **options):
        pass

    def error(self, message, code=1):
        print(message)
        sys.exit(code)