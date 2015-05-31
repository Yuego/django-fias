#coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.conf import settings
from django.core.urlresolvers import reverse
from django.forms import widgets
from django.utils.safestring import mark_safe
from django.utils.translation import get_language, force_text

from django_select2.widgets import get_select2_css_libs, get_select2_heavy_js_libs, HeavySelect2Widget


def convert_to_js_str(val):
    val = force_text(val).replace('\'', '\\\'')
    return u"'%s'" % val


def get_js_libs():
    libs = get_select2_heavy_js_libs()

    if settings.configured and settings.DEBUG:
        libs += ('fias/js/fias.js', )
    else:
        #TODO: сделать минификацию
        libs += ('fias/js/fias.js', )

    lang = get_language()
    if lang in ('ru', 'uk'):
        libs += ('fias/js/locale/select2_locale_{0}.js'.format(lang),)

    return libs


class AddressSelect2(HeavySelect2Widget):
    is_hidden = False

    class Media:
        extend = False
        js = get_js_libs()
        css = {'screen': get_select2_css_libs()}

    options = {
        'width': '50%',
    }

    def render_inner_js_code(self, id_, name, value, attrs=None, choices=(), *args):
        js = super(AddressSelect2, self).render_inner_js_code(id_, name, value, attrs, choices, *args)
        js += ("$('#{0}')"
               ".on('select2-open', fias.onOpen)"
               ".on('select2-selecting', fias.onSelecting)"
               "".format(id_))
        return js

    def render_texts_for_value(self, id_, value, choices):
        if value is not None:
            text = self.field._txt_for_val(value)
            if text:
                return "$('#%s').txt(%s);" % (id_, convert_to_js_str(text))


class AreaChainedSelect(widgets.Select):

    def __init__(self, app_name, model_name, address_field, *args, **kwargs):

        self.app_name = app_name
        self.model_name = model_name
        self.address_field = address_field

        super(AreaChainedSelect, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, choices=()):

        url = reverse('fias:get_areas_list')
        js = """
        <script type="text/javascript">
        //<![CDATA[
            $('#id_%(address_field)s').change(function(){
                var val = $(this).val();
                $("#%(id)s").empty();

                $.getJSON("%(url)s/?guid="+val, function(data){
                    if (data.err === 'nil' && data.results.length > 0) {
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
