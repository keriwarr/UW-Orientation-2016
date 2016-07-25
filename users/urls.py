from django.conf import settings
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^profile', views.profile),
    url(r'^settings', views.user_settings),
    url(r'^register', views.register, name='register'),
]

if settings.ENVIRONMENT == 'development':
    urlpatterns += [
        url(r'^login', views.login, name='login'),
        url(r'^logout', views.logout, name='logout'),
    ]
else:
    urlpatterns += [
        url(r'^login', 'cas.views.login', name='login'),
        url(r'^logout', 'cas.views.logout', name='logout'),
    ]
