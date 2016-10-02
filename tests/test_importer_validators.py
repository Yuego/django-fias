# coding: utf-8
from __future__ import unicode_literals, absolute_import

import datetime
import uuid
from django.test import TestCase

from fias.importer.validators import (
    socr_base_validator,
    common_validator,
    addrobj_validator,
)
from fias.models import *

today = datetime.date.today()
diff = datetime.timedelta(1)
yesterday = today - diff
tomorrow = today + diff

class TestSocrBaseValidator(TestCase):

    def test_scname_empty(self):
        m = SocrBase(scname='', socrname='some')
        self.assertFalse(socr_base_validator(m))

    def test_socrname_empty(self):
        m = SocrBase(scname='some', socrname='')
        self.assertFalse(socr_base_validator(m))

    def test_all_empty(self):
        m = SocrBase(scname='', socrname='')
        self.assertFalse(socr_base_validator(m))

    def test_valid_model(self):
        m = SocrBase(scname='some', socrname='some')
        self.assertTrue(socr_base_validator(m))


class TestCommonValidator(TestCase):

    def test_startdate_tomorrow(self):
        m = AddrObj(startdate=tomorrow, enddate=tomorrow)
        self.assertFalse(common_validator(m, today=today))

    def test_enddate_yesterday(self):
        m = AddrObj(startdate=yesterday, enddate=yesterday)
        self.assertFalse(common_validator(m, today=today))

    def test_both_today(self):
        m = AddrObj(startdate=today, enddate=today)
        self.assertFalse(common_validator(m, today=today))

    def test_valid_model(self):
        m = AddrObj(startdate=yesterday, enddate=tomorrow)
        self.assertTrue(common_validator(m, today=today))


class TestAddrobjValidator(TestCase):

    def test_nextid(self):
        m = AddrObj(startdate=yesterday, enddate=tomorrow, nextid=uuid.uuid4())
        self.assertFalse(addrobj_validator(m, today=today))

    def test_valid(self):
        m = AddrObj(startdate=yesterday, enddate=tomorrow, actstatus=True)
        self.assertTrue(addrobj_validator(m, today=today))
