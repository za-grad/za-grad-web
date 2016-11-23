from django.contrib import admin
from django.template import loader, Context

from .models import *


class IdeaAdmin(admin.ModelAdmin):

    class Media:
        js = ("jquery/jquery.custom.js", "admin/approve_idea.js")

    list_display = ['district', 'title', 'description', 'user',
        'vote_yes_count', 'vote_no_count', 'vote_diff', 'approved', 'approve']
    list_filter = ['district', 'approved', 'category']
    search_fields = ['title', 'description']

    def approve(self, obj):
        t = loader.get_template('admin/idea/_approve.html')
        c = Context({'obj': obj})
        return t.render(c)
    approve.short_description = ''
    approve.allow_tags = True


class IdeaCommentAdmin(admin.ModelAdmin):

    class Media:
        js = ("jquery/jquery.custom.js",)

    def queryset(self, request):
        return super(IdeaCommentAdmin,
            self).queryset(request).exclude(flagged_by=None).filter(banned=None)

    list_display = ['comment', 'ban']
    readonly_fields = ['comment']

    def ban(self, obj):
        t = loader.get_template('admin/comment/_ban.html')
        c = Context({'obj': obj})
        return t.render(c)
    ban.short_description = ''
    ban.allow_tags = True


admin.site.register(IdeaComment, IdeaCommentAdmin)
admin.site.register(Idea, IdeaAdmin)
admin.site.register(IdeaCategory)
admin.site.register(District)
