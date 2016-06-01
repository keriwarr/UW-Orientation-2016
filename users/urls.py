from django.conf import url

urlpatterns = (
    url(r'^users/$', 'views.users_list'),
    url(r'^users/add/$', 'views.users_create'),
    url(r'^users/update/(?P<pk>\d+)?$', 'views.users_update'),
    url(r'^users/delete/(?P<pk>\d+)?$', 'views.users_delete'),
    url(r'^users/detail/(?P<pk>\d+)?$', 'views.users_detail'),
)
