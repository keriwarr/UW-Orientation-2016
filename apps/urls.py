from django.conf.urls import include, url

from apps import views


urlpatterns = [
    url(r'^tie-guard-radio/', include('apps.tie_guard_radio.urls')),
    url(r'^announcements/', include('apps.announcements.urls')),
]
