# coding: utf-8
from __future__ import unicode_literals, absolute_import

import os

DATA_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), 'data'))

FAKE_SOURCE_PATH = os.path.join(DATA_PATH, 'fake')
FAKE_DIR_PATH = os.path.join(FAKE_SOURCE_PATH, 'directory')
FAKE_ARCHIVE_PATH = os.path.join(FAKE_SOURCE_PATH, 'archive.rar')
FAKE_FILES = ('file0', 'file1', 'file2')
