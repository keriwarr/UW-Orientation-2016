def can_play_song(song_metadata):
    if song_metadata is None:
        return False
    elif song_metadata.get('explicit', False):
        return False
    return True
