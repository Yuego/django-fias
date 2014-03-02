#coding: utf-8
from __future__ import unicode_literals, absolute_import

import datetime
import re

table_prefix = 'as_'
table_pattern = r'(?P<deleted>del_)?(?P<name>[a-z]+)_(?P<date>\d+)_(?P<uuid>[a-z0-9-]{36}).xml'
table_re = re.compile(table_prefix + table_pattern, re.I)


class BadTableNameError(Exception):
    pass


class Table(object):

    def __init__(self, archive, filename):
        self._archive = archive
        self._filename = filename
        self._name = None
        self._date = None
        self._uuid = None
        self._is_deleted = False

        self._parse_filename()

    def _parse_filename(self):
        m = table_re.match(self._filename)
        if m is None:
            raise BadTableNameError('Wrong tablename `{0}`'.format(self._filename))
        dict_ = m.groupdict()
        self._is_deleted = not (dict_['deleted'] is None)
        self._name = dict_['name'].lower()
        self._uuid = dict_['uuid'].lower()
        self._date = datetime.datetime.strptime(dict_['date'], "%Y%m%d").date()

    @property
    def name(self):
        return self._name

    @property
    def full_name(self):
        if self.is_deleted:
            return 'del_' + self._name
        else:
            return self.name

    @property
    def date(self):
        return self._date

    @property
    def uuid(self):
        return self._uuid

    @property
    def is_deleted(self):
        return self._is_deleted

    def open(self):
        return self._archive.open(self._filename)

    def __repr__(self):
        return '<Table `{0}`>'.format(self.full_name)
