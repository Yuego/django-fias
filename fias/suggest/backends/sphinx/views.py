# coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.db import connections, OperationalError
from django.http import Http404, JsonResponse
from django.utils.encoding import smart_text
from django.views.generic.list import BaseListView
from django_select2.views import AutoResponseView

from .config import SPHINX_ADDROBJ_INDEX, SEARCHD_CONNECTION
from fias.models import AddrObj

connections.databases['fias_search'] = SEARCHD_CONNECTION


def dict_fetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


class SphinxResponseView(AutoResponseView):

    def get(self, request, *args, **kwargs):
        """
        Return a :class:`.django.http.JsonResponse`.

        Example::

            {
                'results': [
                    {
                        'text': "foo",
                        'id': 123
                    }
                ],
                'more': true
            }

        """
        self.widget = self.get_widget_or_404()
        self.term = kwargs.get('term', request.GET.get('term', ''))
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return JsonResponse({
            'results': [
                {
                    'text': obj['fullname'],
                    'id': obj['aoguid'],
                    #'level': obj['aolevel']
                }
                for obj in context['object_list']
                ],
            'more': context['page_obj'].has_next()
        })

    def get_queryset(self):

        try:
            cur = connections['fias_search'].cursor()

            query = 'SELECT aoguid, fullname FROM {0} WHERE MATCH(%s) ORDER BY item_weight DESC, ' \
                    'weight() DESC LIMIT 0,50 OPTION field_weights=(' \
                    'formalname=100, fullname=80' \
                    ')'.format(SPHINX_ADDROBJ_INDEX)

            cur.execute(query, (self.term + '*',))

            return dict_fetchall(cur)
        except OperationalError:
            return []


class GetAreasListView(BaseListView):

    def get(self, request, *args, **kwargs):
        self.term = kwargs.get('term', request.GET.get('term', ''))
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return JsonResponse({
            'results': [
                {
                    'text': smart_text(obj),
                    'id': obj.pk,
                }
                for obj in context['object_list']
                ],
        })

    def get_queryset(self):
        try:
            address = AddrObj.objects.get(pk=self.term)
        except AddrObj.DoesNotExist:
            return []

        city = self._get_city_obj(address)

        if city is None:
            return []

        return AddrObj.objects.filter(parentguid=city.pk, shortname='р-н')

    def _get_city_obj(self, obj):
        if obj.shortname != 'г' and obj.aolevel > 1:
            parent = AddrObj.objects.get(pk=obj.parentguid)
            return self._get_city_obj(parent)
        elif obj.shortname == 'г':
            return obj
        else:
            return None
