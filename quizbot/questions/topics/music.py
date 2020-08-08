from ..questions import question, answersCount
import random
from .. import utils


@question('music', ['music/albums'])
def yearByAlbum(als):
    album, artist, year = als.sample(1).iloc[0][['album', 'artist', 'year']]
    question = utils.string('yearByAlbum').f(album=album, artist=artist)
    return question, tuple(str(y) for y in utils.years(year))


@question('music', ['music/albums'])
def albumByYear(als):
    right = als.sample(1)
    year = right.year.iloc[0]
    weights = als.year.apply(lambda y: min(abs(y - year), 20) ** 8)
    wrong = als.sample(answersCount() - 1, weights=weights)
    question = utils.string('albumByYear').f(year=year)
    return question, utils.format(right, wrong, utils.string('albumByArtistAnswer').f())


@question('music', ['music/albums', 'music/artists'])
def artistByAlbum(al, ar):
    album, artist, year = al.sample(1).iloc[0][['album', 'artist', 'year']]
    wrongArtists = ar[ar.artist != artist].sample(answersCount() - 1).artist
    question = utils.string('artistByAlbum').f(album=album, year=year)
    return question, (artist, *wrongArtists)


@question('music', ['music/albums'])
def albumByArtist(a):
    album, artist, year = a.sample(1).iloc[0][['album', 'artist', 'year']]
    wrongAlbums = a[a.artist != artist].sample(answersCount() - 1).album
    question = utils.string('albumByArtist').f(artist=artist, year=year)
    return question, (album, *wrongAlbums)


@question('music', ['music/albums', 'music/artists'])
def artistBySong(al, ar):
    songs, artist, year = al.sample(1).iloc[0][['songs', 'artist', 'year']]
    song = random.choice(songs)
    wrongArtists = ar[ar.artist != artist].sample(answersCount() - 1).artist
    question = utils.string('artistBySong').f(song=song, year=year)
    return question, (artist, *wrongArtists)


@question('music', ['music/albums'])
def albumBySong(a):
    right = a.sample(1)
    songs, album, year = right.iloc[0][['songs', 'album', 'year']]
    song = random.choice(songs)
    wrong = a[a.album != album].sample(answersCount() - 1)
    question = utils.string('albumBySong').f(song=song, year=year)
    return question, utils.format(right, wrong, utils.string('albumByArtistAnswer').f())
