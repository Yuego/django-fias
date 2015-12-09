# coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.core.urlresolvers import reverse
from django.forms import widgets
from django.forms.models import ModelChoiceField
from django.utils.safestring import mark_safe

from django_select2.forms import ModelSelect2Widget
from fias.config import SUGGEST_AREA_VIEW


class AddressSelect2Widget(ModelSelect2Widget):
    search_fields = ['parentguid__exact']

    def build_attrs(self, extra_attrs=None, **kwargs):
        attrs = super(AddressSelect2Widget, self).build_attrs(extra_attrs=extra_attrs, **kwargs)

        # Вручную задаем длину поля, чтоб текст был читаем
        attrs.setdefault('style', 'min-width: 300px;')

        return attrs

    def render_options(self, choices, selected_choices):
        if '' in selected_choices:
            selected_choices.pop(selected_choices.index(''))

        choices = ((obj.pk, obj.full_name(5, True)) for obj in self.queryset.filter(pk__in=selected_choices))

        return super(AddressSelect2Widget, self).render_options(choices, selected_choices)


class AddressSelect2Field(ModelChoiceField):
    widget = AddressSelect2Widget

    def __init__(self, queryset, *args, **kwargs):
        super(AddressSelect2Field, self).__init__(queryset, *args, **kwargs)
        # Хак, чтоб виджет не дёргал БД ФИАС
        setattr(self, '_choices', [])


class AreaChainedSelect(widgets.Select):

    def __init__(self, app_name, model_name, address_field, *args, **kwargs):

        self.app_name = app_name
        self.model_name = model_name
        self.address_field = address_field

        super(AreaChainedSelect, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, choices=()):

        url = reverse(SUGGEST_AREA_VIEW)
        js = """
        <script type="text/javascript">
        //<![CDATA[
            $('#id_%(address_field)s').change(function(){
                var val = $(this).val();
                $("#%(id)s").empty();

                $.getJSON("%(url)s?term="+val, function(data){
                    if (data.results.length > 0) {
                        var opts = data.results, options = '';
                        for (var i = 0; i < opts.length; i++) {
                            options += '<option value="' + opts[i].id + '">' + opts[i].text + '</option>';
                        }
                        $("#%(id)s").html(options);
                    }
                });
            });
        //]]>
        </script>
        <span id="abcdef"></span>
        """ % {
            'address_field': self.address_field,
            'url': url,
            'id': attrs['id'],
            }

        output = super(AreaChainedSelect, self).render(name, value, attrs, choices)
        output += js
        return mark_safe(output)


class ChainedAreaField(ModelChoiceField):

    def __init__(self, app_name, model_name, address_field, *args, **kwargs):

        defaults = {
            'widget': AreaChainedSelect(app_name, model_name, address_field)
        }
        defaults.update(kwargs)

        super(ChainedAreaField, self).__init__(*args, **defaults)
