import json
import urllib
from urllib2 import urlopen
from urllib2 import urlparse

API_URL = 'https://api.spotify.com/'
VERSION = 'v1'


def urljoin(*components):
    return '/'.join((u[:-1] if u.endswith('/') else u) for u in components)

def fetch(data):
    formatted = urllib.urlencode(data)
    url = urljoin(API_URL, VERSION, 'search', '?' + formatted)
    f = urlopen(url)
    return json.loads(f.read())

def normalize(name):
    repls = (
        ('"', ''),
        ('-', ''),
        ('~', ''),
        ('\'', ''),
    )
    name = name.encode('ascii', 'ignore')
    for (orig, repl) in repls:
        name = name.replace(orig, repl)
    return name

def fetch_song_data(name, author):
    tracks = fetch(data = {
        'type': 'track',
        'author': author,
        'q': name
    }).get('tracks')

    author = normalize(author)
    songs = tracks.get('items', [])
    for song in songs:
        artists = map(lambda a: a.get('name'), song.get('artists'))
        for artist in artists:
            artist = normalize(artist)
            if author.lower() in artist.lower():
                return song
    return None
