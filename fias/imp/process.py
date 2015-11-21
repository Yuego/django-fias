#coding: utf-8
from __future__ import unicode_literals, absolute_import

import datetime
from django.conf import settings
from django import db


class TableLoader(object):

    def __init__(self, limit=10000):
        self.limit = int(limit)
        self.counter = 0
        self.upd_counter = 0
        self.skip_counter = 0

    def check(self, item):
        if item is None or item.pk is None:
            return False

        if getattr(item, 'nextid', None):
            return False

        today = datetime.date.today()
        if hasattr(item, 'enddate') and item.enddate and item.enddate < today:
            return False

        if hasattr(item, 'startdate') and item.startdate and item.startdate > today:
            return False

        return True

    def create(self, table, objects):
        table.model.objects.bulk_create(objects)

        if settings.DEBUG:
            db.reset_queries()

    def load(self, archive, table):
        objects = []
        for item in table.rows(archive):
            if not self.check(item):
                self.skip_counter += 1
                continue

            objects.append(item)
            self.counter += 1

            if self.counter and self.counter % self.limit == 0:
                self.create(table, objects)
                objects = []
                print ('Created {0} objects'.format(self.counter))

        if objects:
            self.create(table, objects)
            print ('Created {0} objects'.format(self.counter))

        print ('Skipped {0} objects'.format(self.skip_counter))

    def update(self, archive, table):
        model = table.model
        objects = []
        for item in table.rows(archive):
            if not self.check(item):
                self.skip_counter += 1
                continue

            try:
                old_obj = model.objects.filter(pk=item.pk)
            except model.DoesNotExist:
                objects.append(item)
                self.counter += 1
            else:
                if old_obj.updatedate < item.updatedate:
                    item.save()
                    self.upd_counter += 1

            if self.counter and self.counter % self.limit == 0:
                self.create(table, objects)
                objects = []
                print ('Created {0} objects'.format(self.counter))

        if objects:
            self.create(table, objects)
            print ('Created {0} objects'.format(self.counter))

        if self.upd_counter:
            print ('Updated {0} objects'.format(self.upd_counter))

        print ('Skipped {0} objects'.format(self.skip_counter))
