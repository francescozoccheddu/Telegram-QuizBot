from ..quiz import question, answersCount
import random


@question('music', 0, ['music/albums'])
def whatYearByAlbum(a):
    album, artist, year = a.sample(1)[['album', 'artist', 'year']].iloc[0]
    last, wrong = 0, []
    import datetime
    now = datetime.datetime.now().year
    for i in range(answersCount() - 1):
        last += random.randint(7, 13)
        y = random.choice((-last, last)) + year
        if y > now:
            y = year - last
        wrong.append(y)
    return f'When was "{album}" by "{artist}" pubblicated?', (year, *wrong)


@question('music', 0, ['music/albums'])
def whatAlbumByYear(a):
    import pandas
    right = a.sample(1)
    year = right.year.iloc[0]
    weights = a.year.apply(lambda y: min(abs(y - year), 10) ** 8)
    albums = pandas.concat([right, a.sample(answersCount() - 1, weights=weights)])
    answers = albums.apply(lambda row: f'"{row.album}" by "{row.artist}"', axis=1)
    return f'What album was pubblicated in "{year}"?', tuple(answers)


@question('music', 0, ['music/albums', 'music/artists'])
def whatArtistByAlbum(al, ar):
    album, artist, year = al.sample(1)[['album', 'artist', 'year']].iloc[0]
    artists = ar[ar.artist != artist].sample(answersCount() - 1).artist
    return f'Who performed the album "{album}" in {year}?', (artist, *artists)


@question('music', 0, ['music/albums'])
def whatAlbumByArtist(a):
    album, artist, year = a.sample(1)[['album', 'artist', 'year']].iloc[0]
    albums = a[a.artist != artist].sample(answersCount() - 1).album
    return f'What album was made by "{artist}" in {year}?', (album, *albums)
