#coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.utils.text import force_unicode

from django_select2.fields import HeavyModelSelect2ChoiceField

from django_fias import widgets


class AddressSelect2Field(HeavyModelSelect2ChoiceField):

    widget = widgets.AddressSelect2

    def __init__(self, *args, **kwargs):
        super(AddressSelect2Field, self).__init__(*args, **kwargs)
        self.widget.field = self

    def _txt_for_val(self, value):
        obj = self.queryset.get(pk=value)
        lst = [force_unicode(obj)]

        def make_list(o):
            if o.aolevel > 1:
                try:
                    parent = self.queryset.get(aoguid=o.parentguid)
                except self.queryset.model.DoesNotExist:
                    return
                else:
                    lst.append(force_unicode(parent))
                    make_list(parent)

        make_list(obj)
        return ', '.join(lst[::-1])
