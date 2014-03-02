#coding: utf-8
from __future__ import unicode_literals, absolute_import

import datetime


def get_table_uuid():
    return '00000000-0000-0000-0000-000000000000'


def get_table_date_str():
    return '20140101'


def get_table_date():
    return datetime.date(2014, 1, 1)


def get_table_name(name='table'):
    return 'as_{0}_{1}_{2}.xml'.format(name, get_table_date_str(), get_table_uuid()).upper()


def get_bad_table_name(name='table'):
    return 'as_{0}_z_{1}_{2}.xml'.format(name, get_table_date_str(), get_table_uuid()).upper()
