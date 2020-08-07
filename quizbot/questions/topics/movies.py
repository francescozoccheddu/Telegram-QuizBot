from ..questions import question, answersCount
import random
from .. import utils


@question('movies', ['movies/movies', 'movies/directors'])
def whoDirectedMovie(mvs, dcs):
    movie, director, year = mvs.sample(1).iloc[0][['movie', 'director', 'year']]
    wrongDirectors = dcs[dcs.director != director].sample(answersCount() - 1).director
    return f'Who directed the movie "{movie}" in {year}?', (director, *wrongDirectors)


@question('movies', ['movies/movies'])
def whatMovieByDirector(mvs):
    movie, director, year = mvs.sample(1).iloc[0][['movie', 'director', 'year']]
    wrongMovies = mvs[mvs.director != director].sample(answersCount() - 1).movie
    return f'What movie was directed by {director} in {year}?', (movie, *wrongMovies)


@question('movies', ['movies/movies'])
def whatMovieByYear(mvs):
    import pandas
    right = mvs.sample(1)
    year = right.year.iloc[0]
    weights = mvs.year.apply(lambda y: min(abs(y - year), 20) ** 8)
    wrong = mvs.sample(answersCount() - 1, weights=weights)
    return f'What movie was pubblicated in {year}?', utils.format(right, wrong, '"{movie}" by {director}')


@question('movies', ['movies/movies'])
def whatYearByMovie(mvs):
    movie, director, year = mvs.sample(1).iloc[0][['movie', 'director', 'year']]
    return f'When was "{movie}" by {director} pubblicated?', tuple(str(y) for y in utils.years(year))


@question('movies', ['movies/movies'])
def whatMovieByActor(mvs):
    right = mvs.sample(1)
    actors, year = right.iloc[0][['actors', 'year']]
    actor = random.choice(actors)
    wrong = mvs[mvs.actors.apply(lambda a: actor not in a)].sample(answersCount() - 1)
    return f'What {year} movie did {actor} star in?', utils.format(right, wrong, '"{movie}" by {director}')


@question('movies', ['movies/movies'])
def whatActorByMovie(mvs):
    movie, year, director, actors = mvs.sample(1).iloc[0][['movie', 'year', 'director', 'actors']]
    collector = utils.Collector(actors)
    collector.addIterable(mvs.actors)
    return f'Who starred in the {year} movie "{movie}" by {director}?', collector.answers
