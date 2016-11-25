from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

from filebrowser.sites import site

from django.contrib import admin
admin.autodiscover()

handler500 = 'pages.views.server_error'

urlpatterns = patterns('',

    url(r'^admin/members/mass_mail', 'members.admin_views.mass_mail',
        name='members_mass_mail'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'idea.views.homepage', name='home'),
    url(r'', include('pages.urls')),
    url(r'^blog/', include('blog.urls')),
    url(r'^prijedlozi/', include('idea.urls')),
    url(r'^korisnici/', include('members.urls')),
    url(r'^donacije/', include('donations.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/filebrowser/', include(site.urls)),

    url(r'^accounts/login/test/$', 'idea.views.test_login', name='login_test'),

    url(r'^google1fc0cb01e90c2212.html$', 'idea.views.webmaster_tools_html',
        name='webmaster_tools_html'),

)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
    )

urlpatterns += patterns('',
    url(r'^(?P<page_name>[\w-]+)/$', 'pages.views.page_view', name='page_view'),
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
