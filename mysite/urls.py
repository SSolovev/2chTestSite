# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from mysite import settings
from mysite.views import *
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.views import login, logout
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url('^forum/$', categories, name="main"),
    url('^forum/(?P<subcategory_id>\d+)/topic/$', create_thread, name = 'create_topic_page'),
    url('^forum/(?P<subcategory_id>\d+)/(?P<top_id>\d+)/$', thread, name = 'topic_page'),
    url('^forum/(?P<subcategory_id>\d+)/$', thread_list, name = 'threads'),
    url(r'^forum/login/$',  login, name="login_page"),
    url(r'^forum/logout/$', logout,{"next_page":"/forum/"},name="logout_page"),
    url(r'^forum/register/$', register, name="register_page"),
    url(r'^forum/registered/$', direct_to_template, {'template' : 'registration/successful_reg.html'}),
    url(r'^admin/', include(admin.site.urls))
)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()