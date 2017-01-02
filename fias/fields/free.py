# coding: utf-8
from __future__ import unicode_literals, absolute_import

import inspect

from django.contrib.admin.widgets import AdminTextInputWidget
from django.core.urlresolvers import reverse
from django.db.models.fields import CharField
from django import forms
from django.forms import widgets

from fias.config import AUTOCOMPLETE_VIEW


class FreeAddressWidget(widgets.TextInput):

    class Media:
        css = {
            'all': ('fias/jquery-ui-1.12.1-autocomplete/jquery-ui.min.css',),
        }
        js = (
            'fias/jquery-ui-1.12.1-autocomplete/jquery-ui.min.js',
            'fias/autocomplete.js',
        )

    def __init__(self, attrs=None):

        final_attrs = {
            'data-autocomplete': 'address',
        }

        if attrs is not None:
            final_attrs.update(attrs)

        super(FreeAddressWidget, self).__init__(attrs=final_attrs)


class FreeAddressFormField(forms.CharField):

    widget = FreeAddressWidget

    def __init__(self, *args, **kwargs):
        super(FreeAddressFormField, self).__init__(*args, **kwargs)


class FreeAddressField(CharField):

    def __init__(self, *args, fk_name=None, **kwargs):
        self.fk_name = fk_name

        if 'max_length' not in kwargs:
            kwargs['max_length'] = 255

        CharField.__init__(self, *args, **kwargs)

    def formfield(self, **kwargs):

        attrs = {
            'data-fk-field': self.fk_name or '',
            'data-source': reverse(AUTOCOMPLETE_VIEW),
        }

        # Хак для стандартной админки Django
        widget = kwargs.pop('widget', None)
        if issubclass(widget, AdminTextInputWidget):
            attrs['class'] = (attrs.setdefault('class', '') + ' vTextField').strip()

        defaults = {
            'form_class': FreeAddressFormField,
            #'widget': FreeAddressWidget(attrs=attrs)
        }

        defaults.update(kwargs)
        return CharField.formfield(self, **defaults)

