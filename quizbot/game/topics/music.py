from ..quiz import Topic, question, dependency, cachedDependency, answersCount
from ...utils import autosparql, resources
import random

topic = Topic('music')


@cachedDependency
def albums():
    return autosparql.queryByDescriptorResource('topics/music/albums.json')

@question(topic, dependencies=[albums])
def placeholder():
    pass