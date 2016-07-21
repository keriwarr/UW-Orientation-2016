class Song(object):
    def __init__(self, song_data, *args, **kwargs):
        album = song_data.get('album')
        artists = map(lambda a: a.get('name'), song_data.get('artists'))
        self.name = song_data.get('name')
        self.album = album.get('name')
        self.artist = artists[0]
        self.artists = artists
        self.explicit = album.get('explicit')
        self.open_url = album['external_urls']['spotify']
        self.data = song_data

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '%s - %s' % (self.artist, self.name)

    def __eq__(self, other):
        if isinstance(other, Song):
            return (self.name == other.name) and (self.artist == other.artist)
        return False
