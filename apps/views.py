from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound


def applications_index(request):
    return HttpResponse('Applications')
