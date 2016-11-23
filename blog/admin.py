from django.contrib import admin
from django.conf import settings

from .models import *


class BlogEntryAdmin(admin.ModelAdmin):
    list_display = ['title', 'date']

    class Media:
        js = [settings.STATIC_URL + 'grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            settings.STATIC_URL + 'grappelli/tinymce_setup/tinymce_setup.js']


admin.site.register(BlogEntry, BlogEntryAdmin)
admin.site.register(BlogHolder)
