#coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.forms.fields import ChoiceField
from django.forms.models import ModelChoiceField
from django.forms.models import ModelChoiceIterator
from django.utils.encoding import force_text

from django_select2.forms import ModelSelect2Widget


class AddressSelect2Widget(ModelSelect2Widget):

    def render_options(self, choices, selected_choices):
        choices = ((force_text(obj.pk), obj) for obj in self.queryset.filter(pk__in=selected_choices))

        return super(AddressSelect2Widget, self).render_options(choices, selected_choices)

class AddressSelect2Field(ModelChoiceField):

    def __init__(self, queryset, *args, **kwargs):
        super(AddressSelect2Field, self).__init__(queryset, *args, **kwargs)
        setattr(self, '_choices', [])
