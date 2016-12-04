# coding: utf-8
from __future__ import unicode_literals, absolute_import

from optparse import make_option

import django
from django.core.management.base import BaseCommand

DJ_VER = django.VERSION
DJANGO_VERSION = 'old' if DJ_VER[0] == 1 and DJ_VER[1] < 10 else 'new'


class BaseCommandCompatible(BaseCommand):
    arguments_dictionary = {}

    def __init__(self, stdout=None, stderr=None, no_color=False):
        if DJANGO_VERSION == 'old':
            options_list = []
            for command, arguments in self.arguments_dictionary.items():
                options_list.append(make_option(command, **arguments))
            self.option_list = getattr(BaseCommand, 'options_list', tuple()) + tuple(options_list)
        super(BaseCommandCompatible, self).__init__(stdout, stderr, no_color)

    def add_arguments(self, parser):
        for command, arguments in self.arguments_dictionary.items():
            print('Add command: %s' % command)
            parser.add_argument(command, **arguments)

    def handle(self, *args, **options):
        """
        The actual logic of the command. Subclasses must implement
        this method.
        """
        raise NotImplementedError('subclasses of BaseCommand must provide a handle() method')
