# coding: utf-8
from __future__ import unicode_literals, absolute_import

import os
from fias.importer.source.wrapper import SourceWrapper
from ..info import FAKE_FILES, FAKE_DIR_PATH

from datetime import date


class Wrapper(SourceWrapper):

    def __init__(self, source, **kwargs):
        self.source = None

    def get_date_info(self, filename):
        return date(2000, 1, int(filename[-1])+1)

    def get_file_list(self):
        return FAKE_FILES

    def open(self, filename):
        return open(os.path.join(FAKE_DIR_PATH, filename), 'rb')
