import json

import django.contrib.auth as auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login as django_login_view
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.views.decorators.http import require_http_methods

from apps.sorting_hat import sorting_hat
from users.decorators import active_required, require_positions
from users.forms import CustomUserForm, RegistrationForm
from users.models import CustomUser
from users.roles import *
from users.utils import validate_image


@require_http_methods(['GET', 'POST'])
def login(request):
    if request.user.is_authenticated():
        # User is already authenticated, just redirect them to
        # their profile
        return redirect('/users/profile')
    return django_login_view(request)

@login_required
@active_required
@require_http_methods(['GET', 'POST'])
def logout(request):
    if request.user and request.user.is_authenticated():
        auth.logout(request)
    return redirect('/users/login')

@login_required
@active_required
@require_http_methods(['GET'])
def profile(request):
    return redirect('view_team', team_id=request.user.team.id)

@login_required
@active_required
@require_http_methods(['GET', 'POST'])
def user_settings(request):
    context_data = { 'team': request.user.team }
    instance = request.user
    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=instance)
        fname = request.FILES.get('photo', None)
        try:
            if fname is not None:
                validate_image(fname)
                instance.photo = fname
                instance.save()
            elif request.POST.get('photo-clear', None) is not None:
                instance.photo = None
                instance.save()
            return redirect('profile')

        except ValidationError as e:
            if not isinstance(form.non_field_errors, list):
                form.non_field_errors = []
            form.non_field_errors.append(' '.join(e.messages))

        except Exception as e:
            if not isinstance(form.non_field_errors, list):
                form.non_field_errors = []
            form.non_field_errors.append(str(e))

        context_data['form'] = form
    else:
        form = CustomUserForm(instance=instance)
        context_data['form'] = form
    return render(request, 'profile/settings.html', context=RequestContext(request, context_data))

@login_required
@active_required
@require_positions([FOC, MOD])
def register(request):
    """
    Returns the view used for a new user to register.  This view is only staff-accessible because we want to limit
    only staff to being able to sign up new people.  Ideally, this would only be used for signing up those who arrive late
    to Orientation week / forgot to sign up.
    """
    form = RegistrationForm()
    if request.is_ajax():
        # If the request is an AJAX request, then we want to handle
        # the team assignment and return the result as data.
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user_data = form.cleaned_data
            user_data['username'] = user_data['username'].lower()
            user_data['quest_id'] = user_data['username']
            user = None
            users = CustomUser.objects.filter(username__exact=user_data['quest_id'])
            if users.count() > 0:
                user = users[0]
            else:
                user = None

            if user is None or user.team is None:
                team_assignment = sorting_hat.find_pink_tie_team_assignment(user_data)
                user_data.pop('quest_id')
                if user is None:
                    user = CustomUser(**user_data)
                else:
                    user.first_name = user_data['first_name']
                    user.last_name = user_data['last_name']
                user.is_active = True
                user.team = team_assignment
                user.save()
            if user.is_first_year:
                return json_response({ 'valid': True, 'team': user.team.id })
        return json_response({ 'valid': False })
    return render(request, 'registration/register.html', context=RequestContext(request, { 'form' : form, 'team': request.user.team }))

def json_response(response_data):
    return HttpResponse(json.dumps(response_data), content_type="application/json")
