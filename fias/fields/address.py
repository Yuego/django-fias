#coding: utf-8
from __future__ import unicode_literals, absolute_import

import six

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models.fields import Field
from django.db.models.fields.related import ForeignKey

from fias import forms
from fias.config import FIAS_DATABASE_ALIAS, FIAS_SUGGEST_VIEW


class AddressField(ForeignKey):

    def __init__(self, to='fias.AddrObj', **kwargs):
        ForeignKey.__init__(self, to, **kwargs)

    def formfield(self, **kwargs):
        db = kwargs.pop('using', None)
        if isinstance(self.rel.to, six.string_types):
            raise ValueError("Cannot create form field for %r yet, because "
                             "its related model %r has not been loaded yet" %
                             (self.name, self.rel.to))
        defaults = {
            'queryset': self.rel.to._default_manager.using(db),
            'to_field_name': self.rel.field_name,
            'form_class': forms.AddressSelect2Field,
            'data_view': FIAS_SUGGEST_VIEW,
        }
        defaults.update(kwargs)

        return Field.formfield(self, **defaults)

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


class ChainedAreaField(ForeignKey):

    def __init__(self, to, address_field=None, **kwargs):

        if isinstance(to, six.string_types):
            self.app_name, self.model_name = to.split('.')
        else:
            self.app_name = to._meta.app_label
            self.model_name = to._meta.object_name

        self.address_field = address_field
        kwargs.setdefault('blank', True)
        kwargs.setdefault('null', True)

        ForeignKey.__init__(self, to, **kwargs)

    def formfield(self, **kwargs):
        db = kwargs.pop('using', None)
        if isinstance(self.rel.to, six.string_types):
            raise ValueError("Cannot create form field for %r yet, because "
                             "its related model %r has not been loaded yet" %
                             (self.name, self.rel.to))
        defaults = {
            'form_class': forms.ChainedAreaField,
            'queryset': self.rel.to._default_manager.using(db).none(),
            'to_field_name': self.rel.field_name,
            'app_name': self.app_name,
            'model_name': self.model_name,
            'address_field': self.address_field,
        }
        defaults.update(kwargs)

        return super(ChainedAreaField, self).formfield(**defaults)

    def south_field_triple(self):
        from south.modelsinspector import introspector
        args, kwargs = introspector(self)
        return (six.binary_type('fias.fields.address.ChainedAreaField'), args, kwargs)
