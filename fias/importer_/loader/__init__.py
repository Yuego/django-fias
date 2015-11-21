#coding: utf-8
from __future__ import unicode_literals, absolute_import

from importlib import import_module


class UnknownTableError(Exception):
    pass


def _import(name):
    return import_module('fias.importer.loader.{0}'.format(name))


def loader(table):
    try:
        loader_module = _import(table.full_name)
    except ImportError:
        raise UnknownTableError(table.full_name)
    else:
        return loader_module.Loader(table)
