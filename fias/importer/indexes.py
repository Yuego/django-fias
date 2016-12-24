#coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.db import connections
from django.db import models
from django.db.models.fields.related import RelatedField

from fias.config import DATABASE_ALIAS
from fias.compat import get_all_related_objects, get_all_related_many_to_many_objects


def get_simple_field(field):
    params = dict(
        db_index=False,
        primary_key=False,
        unique=field.unique,
        blank=field.blank,
        null=field.null,
    )

    if isinstance(field, models.ForeignKey):
        params.update(dict(
            to=field.rel.to,
        ))
    elif isinstance(field, models.CharField):
        params.update(dict(
            max_length=field.max_length,
        ))
    elif isinstance(field, RelatedField):
        raise NotImplementedError('Only ForeignKey and OneToOne related fields supported')

    simple_field = field.__class__(**params)
    simple_field.column = field.column
    simple_field.model = field.model

    return simple_field


def get_indexed_fields(model):
    for field in model._meta.fields:
        # Не удаляем индекс у первичных ключей и полей,
        # на которые есть ссылки из других моделей
        if field.primary_key and any(
            [rel for rel in get_all_related_objects(model._meta) if rel.field_name == field.name]
        ):
            continue

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
