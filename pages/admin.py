from django.contrib import admin
from django.conf import settings

from .models import *


class PageAdmin(admin.ModelAdmin):
    list_display = ['title', 'content']

    class Media:
        js = [settings.STATIC_URL + 'grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            settings.STATIC_URL + 'grappelli/tinymce_setup/tinymce_setup.js']


class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'content']

    class Media:
        js = [settings.STATIC_URL + 'grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            settings.STATIC_URL + 'grappelli/tinymce_setup/tinymce_setup.js']


class MembershipAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'oib', 'street', 'district', 'phone', 'mobile', 'email', 'role', 'active']
    search_fields = ['first_name', 'last_name', 'oib', 'street', 'district', 'phone', 'mobile', 'email', 'role', 'active']


admin.site.register(Page, PageAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Membership, MembershipAdmin)
