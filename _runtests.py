#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from django.conf import settings
from django.core.management import call_command

sys.path.insert(0, '.')

settings.configure(
    INSTALLED_APPS=('fias',),
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3'
        },
        'fias': {
            'ENGINE': 'django.db.backends.sqlite3'
        },
    },
    SECRET_KEY='key',
    FIAS_DATABASE_ALIAS='fias',
)

if __name__ == "__main__":
    call_command('test', 'fias')
