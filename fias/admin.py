#coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.contrib import admin
from fias.models import SocrBase


class SocrBaseAdmin(admin.ModelAdmin):
    list_display = ['level', 'scname', 'socrname', 'item_weight']
    readonly_fields = ['level', 'scname', 'socrname', 'kod_t_st']
    list_editable = ['item_weight']
    ordering = ['-item_weight', 'level']


admin.site.register(SocrBase, SocrBaseAdmin)
