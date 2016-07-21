from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound


def games_index(request):
    return HttpResponse('Games')


def game_details(request, game_slug):
    return HttpResponse(str(game_slug))
