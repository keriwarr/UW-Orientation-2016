from django.conf.urls import url

urlpatterns = [
    url(r'^announcements/$', 'apps.announcements.views.main', name='announcements'),
    url(r'^announcements/new/$', 'apps.announcements.views.new',
        name='new_announcement'),
    url(r'^announcements/(?P<pk>[0-9]+)/edit/$', 'apps.announcements.views.edit',
        name='edit_announcement'),
]
