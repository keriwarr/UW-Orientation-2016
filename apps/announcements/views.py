from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from django.template import RequestContext
from django.views.decorators.http import require_http_methods

from apps.announcements.models import Announcement
from apps.announcements.forms import AnnouncementForm

from users.decorators import active_required, require_positions
from users.roles import FOC


@login_required
@active_required
@require_http_methods(['GET'])
def main(request):
    max_num_announcements = 1
    announcements = Announcement.objects.all().order_by('-created')
    paginator = Paginator(announcements, max_num_announcements)
    page = int(request.GET.get('page', 1))
    try:
        announcements = paginator.page(page)
    except (InvalidPage, EmptyPage):
        page = 1
        announcements = paginator.page(page)
    context = RequestContext(request, {
        'announcements': announcements,
        'team': request.user.team,
        'num_pages': paginator.num_pages,
        'current_page': page
    })
    return render(request, 'announcements/index.html', context=context)

@login_required
@active_required
@require_positions([FOC])
@require_http_methods(['GET', 'POST'])
def new(request):
    if request.method == 'GET':
        form = AnnouncementForm()
    else:
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            Announcement.objects.create(title=title, text=text)
            return redirect('announcements')
    context = RequestContext(request, { 'form': form, 'team': request.user.team })
    return render(request, 'announcements/edit.html', context=context)

@login_required
@active_required
@require_positions([FOC])
@require_http_methods(['GET', 'POST'])
def edit(request, pk):
    instance = get_object_or_404(Announcement, pk=pk)
    if request.method == 'GET':
        form = AnnouncementForm(instance=instance)
    else:
        form = AnnouncementForm(request.POST, instance=instance)
        if form.is_valid():
            instance.title = form.cleaned_data['title']
            instance.text = form.cleaned_data['text']
            instance.save()
            return redirect('announcements')
    context = RequestContext(request, { 'form': form, 'team': request.user.team, 'announcement': instance })
    return render(request, 'announcements/edit.html', context=context)
