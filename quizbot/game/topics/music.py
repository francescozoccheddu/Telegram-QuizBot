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
