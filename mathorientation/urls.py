from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = (
    url(r'^admin/', include(admin.site.urls)),
    url(r'^teams/', include('teams.urls')),
    url(r'^users/', include('users.urls')),
    url(r'^apps/', include('apps.urls')),
    url(r'^games/', include('games.urls')),
    url(r'', include('apps.announcements.urls')),
    url(r'', include('home.urls')),
)
