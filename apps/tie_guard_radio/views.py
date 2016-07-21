from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext

from apps.tie_guard_radio.forms import SubmissionForm
from apps.tie_guard_radio.radio import (SongError, get_current_song, get_song_queue, request_song)


def tie_guard_radio(request):
    # If this is a POST request, we need to process the data
    form = None
    errors = None
    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            # Try to add the song to the queue
            data = form.cleaned_data
            try:
                request_song(data['song_name'], data['artist_name'])
                return HttpResponseRedirect('/apps/tie-guard-radio/')
            except SongError as e:
                errors = [ str(e) ]
        else:
            errors = [ 'Invalid Form' ]
    else:
        form = SubmissionForm()
    songs = get_song_queue()
    current_song = get_current_song()
    if current_song is not None:
        songs = [current_song] + songs
    return render(request, 'tie_guard_radio/index.html',
        RequestContext(request, {
            'form': form,
            'queue': songs,
            'current_song': current_song,
            'errors': errors
        })
    )
