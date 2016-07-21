from django.conf import settings
from django.conf.urls import url


urlpatterns = [
    url(r'^profile/$', 'users.views.profile', name='profile'),
    url(r'^settings/$', 'users.views.user_settings', name='user_settings'),
    url(r'^register/$', 'users.views.register', name='register'),
]

if settings.ENVIRONMENT == 'development':
    urlpatterns += [
        url(r'^login/$', 'users.views.login', name='login'),
        url(r'^logout/$', 'users.views.logout', name='logout'),
    ]
else:
    urlpatterns += [
        url(r'^login/$', 'cas.views.login', name='login'),
        url(r'^logout/$', 'cas.views.logout', name='logout'),
    ]
