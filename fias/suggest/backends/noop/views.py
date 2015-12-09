# coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.http import JsonResponse
from django.views.generic.list import BaseListView


class EmptyResponseListView(BaseListView):

    def get(self, request, *args, **kwargs):
        return JsonResponse({
            'results': [],
            'more': False
        })
