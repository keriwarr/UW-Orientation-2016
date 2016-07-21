import copy

from .models import Song
from .utils.filters import can_play_song
from .utils.metadata import fetch_song_data


# Queue of the songs waiting to be played.  They are
# popped off one by one.
song_queue = []
current_playing = None


class SongError(Exception):
    pass


def request_song(song_name, song_author):
    song_data = fetch_song_data(song_name, song_author)
    if song_data is None:
        raise SongError('No matching results for "%s"' % song_name)
    elif not can_play_song(song_data):
        raise SongError('Explicit content warning for "%s"' % song_name)
    elif exists_in_queue(song_data):
        raise SongError('Song is already in queue')
    add_song_to_queue(song_data)

def exists_in_queue(song_data):
    new_song = Song(song_data)
    return any(map(lambda song: song == new_song, song_queue))

def add_song_to_queue(song_data):
    song_queue.append(Song(song_data))

def set_current_song(song_name):
    song_index = -1
    for (index, song) in enumerate(song_queue):
        if song.name == song_name:
            song_index = index
            break
    if song_index == -1:
        return False
    song = song_queue.pop(song_index)
    current_playing = song
    return True

def get_current_song():
    return current_playing

def get_song_queue():
    return list(copy.deepcopy(song) for song in song_queue)


if __name__ == "__main__":
    data = fetch_song_data(author=raw_input('Artist Name: '), name=raw_input('Song Name: '))
    print('Can play song? %s' % ('Yes' if can_play_song(data) else 'No'))
