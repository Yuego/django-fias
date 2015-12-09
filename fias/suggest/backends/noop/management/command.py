# coding: utf-8
from __future__ import unicode_literals, absolute_import

# coding: utf-8
from __future__ import unicode_literals, absolute_import

import os
import sys
from optparse import make_option

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Suggest backend config commands'
    usage_str = 'No commands for `noop` backend'

    def handle(self, *args, **options):
        self.error(self.usage_str)

    def error(self, message, code=1):
        print(message)
        sys.exit(code)
