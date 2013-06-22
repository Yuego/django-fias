#coding: utf-8
from __future__ import unicode_literals, absolute_import

import six

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models.fields.related import ForeignKey, ManyToOneRel

from fias import forms
from fias.config import FIAS_DATABASE_ALIAS


class AddressField(ForeignKey):

    def formfield(self, **kwargs):
        db = kwargs.pop('using', None)
        if isinstance(self.rel.to, six.string_types):
            raise ValueError("Cannot create form field for %r yet, because "
                             "its related model %r has not been loaded yet" %
                             (self.name, self.rel.to))
        defaults = {
            'queryset': self.rel.to._default_manager.using(db),
            'to_field_name': self.rel.field_name,
        }
        defaults.update(kwargs)

        return forms.AddressSelect2Field(data_view='fias:suggest', **defaults)

    def validate(self, value, model_instance):
        if self.rel.parent_link:
            return
        super(ForeignKey, self).validate(value, model_instance)
        if value is None:
            return

        using = FIAS_DATABASE_ALIAS if 'fias.routers.FIASRouter' in getattr(settings, 'DATABASE_ROUTERS', []) else None
        qs = self.rel.to._default_manager.using(using).filter(
                **{self.rel.field_name: value}
             )
        qs = qs.complex_filter(self.rel.limit_choices_to)
        if not qs.exists():
            raise ValidationError(self.error_messages['invalid'] % {
                'model': self.rel.to._meta.verbose_name, 'pk': value})

    def south_field_triple(self):
        from south.modelsinspector import introspector
        args, kwargs = introspector(self)
        return (six.binary_type('fias.fields.address.AddressField'), args, kwargs)
