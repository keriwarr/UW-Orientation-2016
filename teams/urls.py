from django.conf.urls import url


urlpatterns = [
    url(r'^(?P<team_id>[0-9]+)/$', 'teams.views.view_team', name='view_team'),
    url(r'^rankings/$', 'teams.views.view_all_team_rankings', name='view_all_team_rankings'),
    # These URLs deal with editing teams, but we have them here as they are part of
    # the internal user site.  Users are able to login and edit some portions of their
    # team data under these views.
    url(r'^(?P<team_id>[0-9]+)/edit/$', 'teams.views.edit_team', name='edit_team'),
    url(r'^(?P<team_id>[0-9]+)/profile/edit$', 'teams.views.edit_team_profile', name='edit_team_profile'),
    url(r'^(?P<team_id>[0-9]+)/cheer/add/$', 'teams.views.add_team_cheer', name='add_team_cheer'),
    url(r'^(?P<team_id>[0-9]+)/cheer/edit/(?P<cheer_id>[0-9]+)/$', 'teams.views.edit_team_cheer', name='edit_team_cheer'),
    url(r'^(?P<team_id>[0-9]+)/cheer/delete/(?P<cheer_id>[0-9]+)/$', 'teams.views.delete_team_cheer', name='delete_team_cheer'),
]
