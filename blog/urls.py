from django.conf.urls.defaults import patterns, url
from .views import *


urlpatterns = patterns('',
    url(r'^comment/(?P<id>\d+)/delete/$', blog_comment_delete,
        name='blog_comment_delete'),

    url(r'^(?P<slug>[\w-]+)/$', entries,
        name='blog_entries'),
    url(r'^(?P<slug>[\w-]+)/(?P<id>\d+)/(?P<title_slug>[\w-]+)/$', entry,
        name='blog_entry'),
    url(r'^(?P<slug>[\w-]+)/sidebar/$', blog_sidebar, name='blog_sidebar'),

    url(r'^(?P<blog_entry_id>\d+)/comment/list/$', blog_comment_list,
        name='blog_comment_list'),
    url(r'^(?P<blog_entry_id>\d+)/comment/add/$', blog_comment_add,
        name='blog_comment_add'),

)
