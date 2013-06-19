#coding: utf-8
from __future__ import unicode_literals, absolute_import

import uuid

from django.db import models


class UUIDField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('default', uuid.uuid4)
        kwargs.setdefault('editable', not kwargs.get('primary_key', False))
        kwargs['max_length'] = 36
        super(UUIDField, self).__init__(*args, **kwargs)

    def get_db_prep_value(self, value, **kwargs):
        return self.to_python(value)

    def db_type(self, connection=None):
        if connection.vendor == 'postgresql':
            return 'uuid'
        return super(UUIDField, self).db_type(connection)

    def to_python(self, value):
        if not value:
            return None
        if not isinstance(value, uuid.UUID):
            value = uuid.UUID(value)
        return value

    def south_field_triple(self):
        from south.modelsinspector import introspector
        args, kwargs = introspector(self)

        return ('fias.fields.UUIDField', args, kwargs)