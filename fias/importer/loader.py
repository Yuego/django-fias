#coding: utf-8
from __future__ import unicode_literals, absolute_import

import datetime
from django.conf import settings
from django import db
from progress.helpers import WritelnMixin
from sys import stderr


class LoadingBar(WritelnMixin):
    file = stderr

    text = 'Table: %(table)s. Loaded: %(loaded)d | Updated: %(updated)d | Skipped:  %(skipped)d'

    loaded = 0
    updated = 0
    skipped = 0
    hide_cursor = False

    def __init__(self, message=None, **kwargs):
        self.table = kwargs.pop('table', 'unknown')
        super(LoadingBar, self).__init__(message=message, **kwargs)

    def __getitem__(self, key):
        if key.startswith('_'):
            return None
        return getattr(self, key, None)

    def update(self, loaded=0, updated=0, skipped=0):
        if loaded:
            self.loaded = loaded
        if updated:
            self.updated = updated
        if skipped:
            self.skipped = skipped

        ln = self.text % self
        self.writeln(ln)


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

    def load(self, tablelist, table):
        bar = LoadingBar(table=table.name)

        objects = []
        for item in table.rows(tablelist=tablelist):
            if not self.check(item):
                self.skip_counter += 1
                continue

            objects.append(item)
            self.counter += 1

            if self.counter and self.counter % self.limit == 0:
                self.create(table, objects)
                objects = []
                bar.update(loaded=self.counter)

        if objects:
            self.create(table, objects)
            bar.update(loaded=self.counter)

        bar.update(skipped=self.skip_counter)
        bar.finish()


class TableUpdater(TableLoader):

    def __init__(self, limit=10000):
        self.upd_limit = limit / 10
        super(TableUpdater, self).__init__(limit=limit)

    def load(self, tablelist, table):
        bar = LoadingBar()

        model = table.model
        objects = []
        for item in table.rows(tablelist=tablelist):
            if not self.check(item):
                self.skip_counter += 1
                continue

            try:
                old_obj = model.objects.filter(pk=item.pk)
            except model.DoesNotExist:
                objects.append(item)
                self.counter += 1
            else:
                if not hasattr(item, 'updatedate') or old_obj.updatedate < item.updatedate:
                    item.save()
                    self.upd_counter += 1

            if self.counter and self.counter % self.limit == 0:
                self.create(table, objects)
                objects = []
                bar.update(loaded=self.counter)

            if self.upd_counter and self.upd_counter % self.upd_limit == 0:
                bar.update(updated=self.upd_counter)

        if objects:
            self.create(table, objects)
            bar.update(loaded=self.counter)

        bar.update(skipped=self.skip_counter)
        bar.finish()
