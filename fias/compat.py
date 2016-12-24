#coding: utf-8
from __future__ import unicode_literals, absolute_import

from optparse import make_option

import django
from django.core.management.base import BaseCommand


DJANGO_VERSION = 'old' if django.VERSION < (1, 10) else 'new'


try:
    from django.utils.importlib import import_module
except ImportError:
    from importlib import import_module

try:
    from urllib.request import urlretrieve
    from urllib.error import HTTPError
except ImportError:
    from urllib import urlretrieve
    HTTPError = IOError

try:
    from django.template.base import TemplateDoesNotExist
except ImportError:
    from django.template.loader import TemplateDoesNotExist


def get_all_related_objects(opts):
    """
    Django 1.8 changed meta api, see
    https://docs.djangoproject.com/en/1.8/ref/models/meta/#migrating-old-meta-api
    https://code.djangoproject.com/ticket/12663
    https://github.com/django/django/pull/3848

    :param opts: Options instance
    :return: list of relations except many-to-many ones
    """
    if django.VERSION < (1, 9):
        return opts.get_all_related_objects()
    else:
        return [r for r in opts.related_objects if not r.field.many_to_many]


def get_all_related_many_to_many_objects(opts):
    """
    Django 1.8 changed meta api, see docstr in compat.get_all_related_objects()

    :param opts: Options instance
    :return: list of many-to-many relations
    """
    if django.VERSION < (1, 9):
        return opts.get_all_related_many_to_many_objects()
    else:
        return [r for r in opts.related_objects if r.field.many_to_many]


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
            parser.add_argument(command, **arguments)

    def handle(self, *args, **options):
        """
        The actual logic of the command. Subclasses must implement
        this method.
        """
        raise NotImplementedError('subclasses of BaseCommand must provide a handle() method')
