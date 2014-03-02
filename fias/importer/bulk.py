#coding: utf-8
from __future__ import unicode_literals, absolute_import

import datetime
from django.conf import settings
from django import db
from fias.importer.log import log


class BulkCreate(object):

    def __init__(self, model, pk, upd_field=None, mode='update'):
        self._mode = 'update'

        self.model = model
        self.pk = pk
        self.upd_field = upd_field
        self._set_mode(mode)

        self.objects = []
        self.counter = 0
        self.upd_counter = 0

    def _set_mode(self, value):
        assert value in ('fill', 'update'), 'Wrong mode `{0}`'.format(value)
        self._mode = value

    def _get_mode(self):
        return self._mode

    mode = property(fset=_set_mode, fget=_get_mode)

    def reset_counters(self):
        self.upd_counter = 0
        self.counter = 0

    def _lower_keys(self, d):
        return dict((k.lower(), v) for k, v in d.iteritems())

    def _create(self):
        self.model.objects.bulk_create(self.objects)
        self.objects = []
        if settings.DEBUG:
            db.reset_queries()

    def push(self, raw_data, related_attrs=None):
        data = self._lower_keys(raw_data.attrib)

        if isinstance(related_attrs, dict):
            data.update(related_attrs)

        key = data[self.pk]

        if self.mode == 'fill' or not self.model.objects.filter(**{self.pk: key}).exists():
            self.objects.append(self.model(**data))
            self.counter += 1
        elif self.upd_field is not None and self.upd_field in data:
            old_obj = self.model.objects.get(**{self.pk: key})
            data[self.upd_field] = datetime.datetime.strptime(data[self.upd_field], "%Y-%m-%d").date()

            if getattr(old_obj, self.upd_field) < data[self.upd_field]:
                for k, v in data.items():
                    setattr(old_obj, k, v)
                old_obj.save()
                self.upd_counter += 1

            """
            При обновлении выполняется очень много SELECT-запросов,
            которые тоже неслабо отъедают память.
            Так что лучше почаще чистить лог.
            """
            if settings.DEBUG:
                db.reset_queries()

        del data

        if self.counter and self.counter % 10000 == 0:
            self._create()
            log.info('Created {0} objects'.format(self.counter))

    def finish(self):
        if self.objects:
            self._create()

        if self.upd_counter:
            log.info('Updated {0} objects'.format(self.upd_counter))
