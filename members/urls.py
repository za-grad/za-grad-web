from django.conf.urls.defaults import patterns, url
from .views import *


urlpatterns = patterns('',

    url(r'^uredi/$', profile_edit, name='members_edit_profile'),
    url(r'^(?P<id>\d+)/detalji/$', details, name='members_details'),

    url(r'^$', member_list, name='member_list'),

    url(r'^list/ajax/$', member_list_ajax, name='member_list_ajax'),

    url(r'^mobile_form_handler/$', mobile_form_handler,
        name='member_mobile_form_handler'),

    url(r'^broj-mobitela/$', give_mobile_page,
        name='member_give_mobile_page'),

)
