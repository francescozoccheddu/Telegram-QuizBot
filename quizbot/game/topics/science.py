from ..quiz import Topic, question, dependency, cachedDependency, answersCount
from ...utils import autosparql, resources
import random

topic = Topic('science')


@cachedDependency
def chemicalElements():
    return autosparql.queryByDescriptorResource('topics/science/chemicalElements.json')

@question(topic, dependencies=[chemicalElements])
def placeholder():
    pass