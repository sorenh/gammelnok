from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gammelnok.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^signup/edit/(?P<uuid>\S+)/$', 'event.views.signup_edit', name='signup_edit'),
    url(r'^signup/list/(?P<event_id>\S+)/$', 'event.views.list_attendees', name='list_attendees'),
    url(r'^signup/(?P<event_id>\S+)/$', 'event.views.signup', name='signup'),
    url(r'^signup/', 'event.views.signup_top', name='signup_top'),
    url(r'^$', 'event.views.front', name='front'),
    url(r'^thanks/(?P<event_id>\S+)/$', 'event.views.thanks', name='thanks'),
    url(r'^admin/', include(admin.site.urls)),
)
