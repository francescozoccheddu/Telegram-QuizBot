from ..quiz import Topic, question, dependency, cachedDependency, answersCount
from ...utils import autosparql, resources
import random

topic = Topic('movies')


@cachedDependency
def movies():
    return autosparql.queryByDescriptorResource('topics/movies/movies.json')

@cachedDependency
def directors():
    return autosparql.queryByDescriptorResource('topics/movies/directors.json')


@question(topic, dependencies=[movies, directors])
def placeholder():
    pass