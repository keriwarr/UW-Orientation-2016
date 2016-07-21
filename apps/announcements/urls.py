from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^announcements/', views.main),
    url(r'^announcements/new/$', views.new,
        name='new_announcement'),
    url(r'^announcements/(?P<pk>[0-9]+)/edit/$', views.edit,
        name='edit_announcement'),
]
