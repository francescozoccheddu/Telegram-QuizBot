from ..questions import question, answersCount
import random
from .. import utils


@question('movies', ['movies/movies', 'movies/directors'])
def directorByMovie(mvs, dcs):
    movie, director, year = mvs.sample(1).iloc[0][['movie', 'director', 'year']]
    wrongDirectors = dcs[dcs.director != director].sample(answersCount() - 1).director
    question = utils.string('directorByMovie').f(movie=movie, year=year)
    return question, (director, *wrongDirectors)


@question('movies', ['movies/movies'])
def movieByDirector(mvs):
    movie, director, year = mvs.sample(1).iloc[0][['movie', 'director', 'year']]
    wrongMovies = mvs[mvs.director != director].sample(answersCount() - 1).movie
    question = utils.string('movieByDirector').f(director=director, year=year)
    return question, (movie, *wrongMovies)


@question('movies', ['movies/movies'])
def movieByYear(mvs):
    import pandas
    right = mvs.sample(1)
    year = right.year.iloc[0]
    weights = mvs.year.apply(lambda y: min(abs(y - year), 20) ** 8)
    wrong = mvs.sample(answersCount() - 1, weights=weights)
    question = utils.string('movieByYear').f(year=year)
    return question, utils.format(right, wrong, utils.string('movieByDirectorAnswer').s)


@question('movies', ['movies/movies'])
def yearByMovie(mvs):
    movie, director, year = mvs.sample(1).iloc[0][['movie', 'director', 'year']]
    question = utils.string('yearByMovie').f(movie=movie, director=director)
    return question, tuple(str(y) for y in utils.years(year))


@question('movies', ['movies/movies'])
def movieByActor(mvs):
    right = mvs.sample(1)
    actors, year = right.iloc[0][['actors', 'year']]
    actor = random.choice(actors)
    wrong = mvs[mvs.actors.apply(lambda a: actor not in a)].sample(answersCount() - 1)
    question = utils.string('movieByActor').f(actor=actor, year=year)
    return question, utils.format(right, wrong, utils.string('movieByDirectorAnswer').s)


@question('movies', ['movies/movies'])
def actorByMovie(mvs):
    movie, year, director, actors = mvs.sample(1).iloc[0][['movie', 'year', 'director', 'actors']]
    collector = utils.Collector(actors)
    collector.addIterable(mvs.actors)
    question = utils.string('actorByMovie').f(movie=movie, year=year, director=director)
    return question, collector.answers
