#coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.forms.widgets import HiddenInput
from django.utils.safestring import mark_safe

from django_select2.util import convert_to_js_str
from django_select2.widgets import HeavySelect2Widget


def get_select2_js_libs():
    from django.conf import settings
    if settings.configured and settings.DEBUG:
        return ('fias/js/select2/select2.js', )
    else:
        return ('fias/js/select2/select2.min.js', )


def get_select2_heavy_js_libs():
    libs = get_select2_js_libs()

    from django.conf import settings
    if settings.configured and settings.DEBUG:
        return libs + ('js/heavy_data.js', )
    else:
        return libs + ('js/heavy_data.min.js', )


def get_js_libs():
    libs = get_select2_heavy_js_libs()

    from django.conf import settings
    if settings.configured and settings.DEBUG:
        return libs + ('fias/js/fias.js', )
    else:
        #TODO: сделать минификацию
        return libs + ('fias/js/fias.js', )


def get_select2_css_libs(light=False):
    from django.conf import settings

    if settings.configured and settings.DEBUG:
        return ('fias/js/select2/select2.css', 'css/extra.css',)
    else:
        return ('fias/js/select2/select2.css',)


class AddressSelect2(HeavySelect2Widget):

    class Media:
        extend = False
        js = get_js_libs()
        css = {'screen': get_select2_css_libs()}

    options = {
        'width': '50%',
        'allowClear': True,

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
                return u"$('#%s').txt(%s);" % (id_, convert_to_js_str(text))
