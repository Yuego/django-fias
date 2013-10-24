
from django.contrib import admin

from tst.models import *


class ItemAdmin(admin.ModelAdmin):
    class Media:
        js = ['//ajax.googleapis.com/ajax/libs/jquery/1.10.1/jquery.js']

admin.site.register(Item, ItemAdmin)
admin.site.register(CachedAddress, ItemAdmin)
admin.site.register(CachedAddressWithArea, ItemAdmin)
admin.site.register(CachedAddressWithHouse, ItemAdmin)
admin.site.register(NullableAddressItem, ItemAdmin)
