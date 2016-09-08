# coding: utf-8
from __future__ import unicode_literals, absolute_import

import datetime
import os
import shutil


class SourceWrapper(object):
    source = None

    def __init__(self, source, **kwargs):
        pass

    def get_date_info(self, filename):
        raise NotImplementedError()

    def get_file_list(self):
        raise NotImplementedError()

    def open(self, filename):
        raise NotImplementedError()


class DirectoryWrapper(SourceWrapper):
    is_temporary = False

    def __init__(self, source, is_temporary=False, **kwargs):
        super(DirectoryWrapper, self).__init__(source=source, **kwargs)
        self.is_temporary = is_temporary
        self.source = os.path.abspath(source)

    def get_date_info(self, filename):
        st = os.stat(os.path.join(self.source, filename))
        return datetime.datetime.fromtimestamp(st.st_mtime)

    def get_file_list(self):
        return [f for f in os.listdir(self.source) if (
            not f.startswith('.') and
            os.path.isfile(os.path.join(self.source, f))
        )]

    def get_full_path(self, filename):
        return os.path.join(self.source, filename)

    def open(self, filename):
        return open(self.get_full_path(filename), 'rb')

    def __del__(self):
        if self.is_temporary:
            shutil.rmtree(self.source, ignore_errors=True)


class RarArchiveWrapper(SourceWrapper):

    def __init__(self, source, **kwargs):
        super(RarArchiveWrapper, self).__init__(source=source, **kwargs)
        self.source = source

    def get_date_info(self, filename):
        info = self.source.getinfo(filename)
        return datetime.date(*info.date_time[0:3])

    def get_file_list(self):
        return self.source.namelist()

    def open(self, filename):
        return self.source.open(filename)
