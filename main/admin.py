from django.contrib import admin

from .models import BirthDay, IP, BDayIP


class BirthDayAdmin(admin.ModelAdmin):
    list_display = ('birthday',)
    readonly_fields = ('birthday',)
    list_display_links = None


class IPAdmin(admin.ModelAdmin):
    list_display = ('ip', 'count', 'comment',)
    readonly_fields = ('ip', 'count',)
    list_display_links = ('comment',)
    search_fields = ('comment',)
    # list_editable = ('comment',)


class BDayIPAdmin(admin.ModelAdmin):
    list_display = ('birth_day', 'ip', 'requested_at',)
    readonly_fields = ('birth_day', 'ip', 'requested_at',)
    list_display_links = None
    # empty_value_display = '-- NO COMMENT ---'
    # list_select_related = True
    # list_select_related = ('ip__comment',)


admin.site.register(BirthDay, BirthDayAdmin)
admin.site.register(IP, IPAdmin)
admin.site.register(BDayIP, BDayIPAdmin)
