import itertools

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext
from django.views.decorators.http import require_http_methods

from teams.forms import TeamProfileForm, TeamCheerForm
from teams.models import Team, TeamProfile, TeamCheer
from teams.utils import teams_get_rankings

from users.decorators import require_positions, active_required
from users.models import CustomUser
from users.roles import *


@login_required
@active_required
@require_http_methods(['GET'])
def view_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    user = request.user
    context_data = {}

    if user.position not in [FOC, MOD]:
        if user.team != team:
            raise PermissionDenied

    # We want to show the leaders in the template, so we want the
    # leaders of this team, followed by MODs, followed by FOC
    leaders = list(itertools.chain(team.leaders,
        CustomUser.objects.filter(position=MOD),
        CustomUser.objects.filter(position=FOC)))

    context_data['team'] = team
    context_data['leaders'] = leaders

    return render(request, 'profile/index.html', context=RequestContext(request, context_data))

@login_required
@active_required
@require_http_methods(['GET'])
def view_all_teams(request):
    return render(request, 'profile/team/all.html',
        context=RequestContext(request, {
            'team': request.user.team
        })
    )

@login_required
@active_required
@require_http_methods(['GET'])
def view_all_team_rankings(request):
    return render(request, 'profile/team/rankings.html',
        context=RequestContext(request, {
            'team': request.user.team,
            'rankings': teams_get_rankings()
        })
    )

@login_required
@active_required
@require_http_methods(['GET', 'POST'])
@require_positions([HEAD_LEADER, FOC, MOD])
def edit_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    profile = team.profile

    # Create the profile for the Team if it does not yet exist.
    if profile is None:
        profile = TeamProfile()
        profile.save()
        team.profile = profile
        team.save()

    if request.user.position == HEAD_LEADER:
        if not request.user.team == team:
            raise PermissionDenied

    return render(request, 'profile/team/index.html',
        context=RequestContext(request, { 'team': team }))

@login_required
@active_required
@require_http_methods(['GET', 'POST'])
@require_positions([HEAD_LEADER, FOC, MOD])
def edit_team_profile(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    profile = team.profile
    context_data = { 'team': team }

    if request.user.position == HEAD_LEADER:
        if not request.user.team == team:
            raise PermissionDenied
    elif request.method == 'GET':
        # Create a profile form using the existing profile
        # from the TeamProfile model
        form = TeamProfileForm(instance=profile)
        context_data['form'] = form
    elif request.method == 'POST':
        # Process the data from the form
        form = TeamProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('edit_team', team_id=team.id)
        context_data['form'] = form
    return render(request, 'profile/team/edit.html',
        context=RequestContext(request, context_data))

@login_required
@active_required
@require_http_methods(['GET', 'POST'])
@require_positions([HEAD_LEADER, FOC, MOD])
def add_team_cheer(request, team_id):
    return edit_team_cheer(request, team_id)

@login_required
@active_required
@require_http_methods(['GET', 'POST'])
@require_positions([HEAD_LEADER, FOC, MOD])
def edit_team_cheer(request, team_id, cheer_id=None):
    team = get_object_or_404(Team, pk=team_id)
    context_data = { 'team': team }
    if cheer_id is not None:
        cheer_id = int(cheer_id)

    if request.user.position == HEAD_LEADER:
        if not request.user.team == team:
            raise PermissionDenied
    elif request.method == 'GET':
        # If the cheer_id is not None, then we want to grab that cheer
        # to populate our initial form data, otherwise we are creating
        # a new one.
        cheers = team.profile.cheers.all()
        if (cheer_id is None) or (cheer_id >= len(cheers)):
            form = TeamCheerForm()
            context_data['form'] = form
        else:
            form = TeamCheerForm(instance=cheers[cheer_id])
            context_data['form'] = form
    else:
        # Posting the data for a cheer.  Validate that the data is correct
        # and use it to create the cheer.
        form = None
        cheers = team.profile.cheers.all()
        if cheer_id is None or cheer_id >= len(cheers):
            form = TeamCheerForm(request.POST)
        else:
            form = TeamCheerForm(request.POST, instance=cheers[cheer_id])

        if not form.is_valid():
            context_data['form'] = form
        else:
            instance = form.save(commit=False)
            instance.profile = team.profile
            instance.save()
            return redirect('edit_team', team_id=team_id)

    return render(request, 'profile/team/cheers.html', context=RequestContext(request, context_data))

@login_required
@active_required
@require_http_methods(['GET', 'POST'])
@require_positions([HEAD_LEADER, FOC, MOD])
def delete_team_cheer(request, team_id, cheer_id):
    team = get_object_or_404(Team, pk=team_id)
    if request.user.position == HEAD_LEADER:
        if not request.user.team == team:
            raise PermissionDenied

    profile = team.profile
    cheer_id = int(cheer_id)
    cheers = profile.cheers.all()
    if profile and len(cheers) > cheer_id:
        cheers[cheer_id].delete()

    if request.META.get('HTTP_REFERER', None) is not None:
        return redirect(request.META.get('HTTP_REFERER'))

    return redirect('edit_team', team_id=team_id)
