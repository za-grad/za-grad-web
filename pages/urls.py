from django.conf.urls.defaults import patterns, url

from .views import *

pages_prefix = "stranice"
news_prefix = "novosti"

urlpatterns = patterns('',

    # url(r'^%s/ajax/list/$' % pages_prefix, pages_list, name='pages_list'),
    url(r'^%s/(?P<page_name>[\w-]+)/partial/$' % pages_prefix,
        'pages.views.page_view_as_partial', name='page_view_as_partial'),
    url(r'^%s/ajax/sidebar_list/$' % pages_prefix, sidebar_pages_list,
        name='pages_sidebar_list'),

    url(r'^kontakt/$', contact_page, name='contact_page'),
    url(r'^uclani-se/$', membership_form_page, name='membership_form_page'),

    url(r'^%s/(?P<news_id>\d+)/$' % news_prefix, news_view, name='news_view'),
    url(r'^%s/$' % news_prefix, news_list_page, name='news_list_page'),
    url(r'^%s/list/$' % news_prefix, news_list, name='news_list'),

)
