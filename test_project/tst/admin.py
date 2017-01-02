
from django.contrib import admin

from .models import *


class ItemAdmin(admin.ModelAdmin):
    class Media:
        js = ['//code.jquery.com/jquery-3.1.1.min.js']

admin.site.register(Item, ItemAdmin)
admin.site.register(ItemWithArea, ItemAdmin)
admin.site.register(FreeAddressItem, ItemAdmin)
