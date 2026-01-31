from django.contrib import admin

from .models import BirthDay, IP, BDayIP

admin.site.register(BirthDay)
admin.site.register(IP)
admin.site.register(BDayIP)
