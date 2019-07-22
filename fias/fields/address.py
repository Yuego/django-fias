# coding: utf-8
from __future__ import unicode_literals, absolute_import

import six

from django.core.exceptions import ValidationError
from django.db import router
from django.db import models
from django.db.models.fields import Field
from django.db.models.fields.related import ForeignKey

from fias import forms
from fias.config import SUGGEST_VIEW


class AddressField(ForeignKey):

    def __init__(self, to='fias.AddrObj', on_delete=models.CASCADE, **kwargs):
        kwargs.setdefault('related_name', '+')
        ForeignKey.__init__(self, to, on_delete, **kwargs)

    def formfield(self, **kwargs):
        db = kwargs.pop('using', None)
        if isinstance(self.remote_field.model, six.string_types):
            raise ValueError("Cannot create form field for %r yet, because "
                             "its related model %r has not been loaded yet" %
                             (self.name, self.remote_field.model))

        defaults = {
            'form_class': forms.AddressSelect2Field,
            'widget': forms.AddressSelect2Widget(
                queryset=self.remote_field.model._default_manager.using(db),
                data_view=SUGGEST_VIEW,
            ),
            'queryset': self.remote_field.model._default_manager.using(db),
            'to_field_name': self.remote_field.field_name,
        }
        defaults.update(kwargs)

        return Field.formfield(self, **defaults)

    def validate(self, value, model_instance):
        if self.remote_field.parent_link:
            return
        super(ForeignKey, self).validate(value, model_instance)
        if value is None:
            return

        using = router.db_for_read(self.remote_field.model)
        qs = self.remote_field.model._default_manager.using(using).filter(
            **{self.remote_field.field_name: value}
        )
        qs = qs.complex_filter(self.remote_field.limit_choices_to)
        if not qs.exists():
            raise ValidationError(self.error_messages['invalid'] % {
                'model': self.remote_field.model._meta.verbose_name, 'pk': value})


class ChainedAreaField(ForeignKey):

    def __init__(self, to, on_delete,  address_field=None, **kwargs):

        if isinstance(to, six.string_types):
            self.app_name, self.model_name = to.split('.')
        else:
            self.app_name = to._meta.app_label
            self.model_name = to._meta.object_name

        self.address_field = address_field
        kwargs.setdefault('blank', True)
        kwargs.setdefault('null', True)
        kwargs.setdefault('related_name', '+')

        ForeignKey.__init__(self, to, on_delete, **kwargs)

    def formfield(self, **kwargs):
        db = kwargs.pop('using', None)
        if isinstance(self.remote_field.model, six.string_types):
            raise ValueError("Cannot create form field for %r yet, because "
                             "its related model %r has not been loaded yet" %
                             (self.name, self.remote_field.model))
        defaults = {
            'form_class': forms.ChainedAreaField,
            'queryset': self.remote_field.model._default_manager.using(db).none(),
            'to_field_name': self.remote_field.field_name,
            'app_name': self.app_name,
            'model_name': self.model_name,
            'address_field': self.address_field,
        }
        defaults.update(kwargs)

        return super(ChainedAreaField, self).formfield(**defaults)
