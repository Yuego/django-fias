#coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.db import connections
from django.db.models import ForeignKey
from django.db.models.fields.related import RelatedField

from fias.config import DATABASE_ALIAS


def get_simple_field(field):
    if isinstance(field, ForeignKey):
        simple_field = ForeignKey(
            to=field.rel.to,
            db_index=False,
            primary_key=False,
            unique=False,
        )
    elif isinstance(field, RelatedField):
        raise NotImplementedError('Only ForeignKey and OneToOne related fields supported')
    else:
        simple_field = field.__class__(
            db_index=False,
            primary_key=False,
            unique=False,
        )
    simple_field.column = field.column
    simple_field.model = field.model

    return simple_field


def get_indexed_fields(model):
    for field in model._meta.fields:
        if field.db_index or field.unique:
            yield field, get_simple_field(field)


def change_indexes_for_model(model, field_from, field_to):
    con = connections[DATABASE_ALIAS]
    ed = con.schema_editor()
    ed.alter_field(model, field_from, field_to)


def remove_indexes_from_model(model):
    for field, simple_field in get_indexed_fields(model=model):
        change_indexes_for_model(model=model, field_from=field, field_to=simple_field)


def restore_indexes_for_model(model):
    for field, simple_field in get_indexed_fields(model=model):
        change_indexes_for_model(model=model, field_from=simple_field, field_to=field)
