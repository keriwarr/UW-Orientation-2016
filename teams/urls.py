from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^(?P<team_id>[0-9]+)/$', view_team),
    url(r'^rankings/$', view_all_team_rankings),
    # These URLs deal with editing teams, but we have them here as they are part of
    # the internal user site.  Users are able to login and edit some portions of their
    # team data under these views.
    url(r'^(?P<team_id>[0-9]+)/edit/$', edit_team),
    url(r'^(?P<team_id>[0-9]+)/profile/edit$', edit_team_profile),
    url(r'^(?P<team_id>[0-9]+)/cheer/add/$', add_team_cheer),
    url(r'^(?P<team_id>[0-9]+)/cheer/edit/(?P<cheer_id>[0-9]+)/$', edit_team_cheer),
    url(r'^(?P<team_id>[0-9]+)/cheer/delete/(?P<cheer_id>[0-9]+)/$', delete_team_cheer),
]
