from django.contrib import admin

from .models import *


class MobilePhoneAdmin(admin.ModelAdmin):
    list_display = ['number']


admin.site.register(MobilePhone, MobilePhoneAdmin)
