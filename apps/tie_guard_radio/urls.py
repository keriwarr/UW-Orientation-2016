from django.conf.urls import url

from apps.tie_guard_radio import views


urlpatterns = [
    url(r'^$', views.tie_guard_radio)
]
