#coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.forms.models import ModelChoiceField

from django_select2.fields import HeavyModelSelect2ChoiceField

from fias import widgets


class AddressSelect2Field(HeavyModelSelect2ChoiceField):

    widget = widgets.AddressSelect2

    def __init__(self, *args, **kwargs):
        super(AddressSelect2Field, self).__init__(*args, **kwargs)
        self.widget.field = self

    def _txt_for_val(self, value):
        if not value:
            return
        obj = self.queryset.get(pk=value)
        return obj.full_name(5, True)


class ChainedAreaField(ModelChoiceField):

    def __init__(self, app_name, model_name, address_field, *args, **kwargs):

        defaults = {
            'widget': widgets.AreaChainedSelect(app_name, model_name, address_field)
        }
        defaults.update(kwargs)

        super(ChainedAreaField, self).__init__(*args, **defaults)
