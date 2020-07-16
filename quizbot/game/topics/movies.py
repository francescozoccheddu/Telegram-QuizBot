from ..quiz import question, answersCount
from ...utils import questions
import random


@question('movies', 0, ['movies/movies', 'movies/directors'])
def whoDirectedMovie(mvs, dcs):
    movie, director, year = mvs.sample(1).iloc[0][['movie', 'director', 'year']]
    wrongDirectors = dcs[dcs.director != director].sample(answersCount() - 1).director
    return f'Who directed the movie "{movie}" in {year}?', (director, *wrongDirectors)


@question('movies', 0, ['movies/movies'])
def whatMovieByDirector(mvs):
    movie, director, year = mvs.sample(1).iloc[0][['movie', 'director', 'year']]
    wrongMovies = mvs[mvs.director != director].sample(answersCount() - 1).movie
    return f'What movie was directed by "{director}" in "{year}"?', (movie, *wrongMovies)


@question('movies', 0, ['movies/movies'])
def whatMovieByYear(mvs):
    import pandas
    right = mvs.sample(1)
    year = right.year.iloc[0]
    weights = mvs.year.apply(lambda y: min(abs(y - year), 20) ** 8)
    wrong = mvs.sample(answersCount() - 1, weights=weights)
    return f'What movie was pubblicated in "{year}"?', questions.format(right, wrong, '"{movie}" by "{director}"')


@question('movies', 0, ['movies/movies'])
def whatYearByMovie(mvs):
    movie, director, year = mvs.sample(1).iloc[0][['movie', 'director', 'year']]
    return f'When was "{movie}" by "{director}" pubblicated?', questions.years(year)


@question('movies', 0, ['movies/movies'])
def whatMovieByActor(mvs):
    right = mvs.sample(1)
    actors, year = right.iloc[0][['actors', 'year']]
    actor = random.choice(actors)
    wrong = mvs[mvs.actors.apply(lambda a: actor not in a)].sample(answersCount() - 1)
    return f'What {year} movie did {actor} star in?', questions.format(right, wrong, '"{movie}" by "{director}"')


@question('movies', 0, ['movies/movies'])
def whatActorByMovie(mvs):
    movie, year, director, actors = mvs.sample(1).iloc[0][['movie', 'year', 'director', 'actors']]
    actor = random.choice(actors)
    wrongActors = set()
    for movieActors in mvs.actors:
        wrongActors.update(movieActors)
    wrongActors.discard(actor)
    wrongActors = random.choices(list(wrongActors), k=answersCount()-1)
    return f'Who starred in the {year} movie "{movie}" by "{director}"?', (actor, wrongActors)
