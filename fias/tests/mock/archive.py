#coding: utf-8
from __future__ import unicode_literals, absolute_import

test_archive = 'fias/tests/data/fias.rar'
import rarfile

class Archive(object):

    def __init__(self, *args, **kwargs):
        self._archive = rarfile.RarFile(test_archive)

    def open(self, filename):
        return self._archive.open(filename)
