from ..quiz import question, answersCount
from ...utils import questions
import random



@question('music', 0, ['music/albums'])
def whatYearByAlbum(als):
    album, artist, year = als.sample(1).iloc[0][['album', 'artist', 'year']]
    return f'When was "{album}" by {artist} pubblicated?', questions.years(year)


@question('music', 0, ['music/albums'])
def whatAlbumByYear(als):
    right = als.sample(1)
    year = right.year.iloc[0]
    weights = als.year.apply(lambda y: min(abs(y - year), 20) ** 8)
    wrong = als.sample(answersCount() - 1, weights=weights)
    return f'What album was pubblicated in {year}?', questions.format(right, wrong, '"{album}" by {artist}')


@question('music', 0, ['music/albums', 'music/artists'])
def whatArtistByAlbum(al, ar):
    album, artist, year = al.sample(1).iloc[0][['album', 'artist', 'year']]
    wrongArtists = ar[ar.artist != artist].sample(answersCount() - 1).artist
    return f'Who performed the album "{album}" in {year}?', (artist, *wrongArtists)


@question('music', 0, ['music/albums'])
def whatAlbumByArtist(a):
    album, artist, year = a.sample(1).iloc[0][['album', 'artist', 'year']]
    wrongAlbums = a[a.artist != artist].sample(answersCount() - 1).album
    return f'What album was made by {artist} in {year}?', (album, *wrongAlbums)


@question('music', 0, ['music/albums', 'music/artists'])
def whatArtistBySong(al, ar):
    songs, artist, year = al.sample(1).iloc[0][['songs', 'artist', 'year']]
    song = random.choice(songs)
    wrongArtists = ar[ar.artist != artist].sample(answersCount() - 1).artist
    return f'Who performed the song "{song}" in {year}?', (artist, *wrongArtists)


@question('music', 0, ['music/albums'])
def whatAlbumBySong(a):
    right = a.sample(1)
    songs, album, year = right.iloc[0][['songs', 'album', 'year']]
    song = random.choice(songs)
    wrong = a[a.album != album].sample(answersCount() - 1)
    return f'What album contained the song "{song}" in {year}?', questions.format(right, wrong, '"{album}" by {artist}')
