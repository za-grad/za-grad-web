from django.conf.urls.defaults import patterns, url
from .views import *


urlpatterns = patterns('',

    url(r'^doniraj/$', donate, name='donations_donate'),

)
