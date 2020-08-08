from ..questions import question
import random
from .. import utils


def _similarity(a, b):
    from nltk.metrics.distance import jaro_winkler_similarity
    return jaro_winkler_similarity(a, b)


def _similarityMap(target, offset=0):
    return lambda v: _similarity(target, v) + offset


@question('science', ['science/chemicalElements'])
def chemicalElementBySymbol(els):
    name, symbol = els.sample(1).iloc[0]
    collector = utils.Collector(name)
    collector.add(els.name, weights=els.name.map(_similarityMap(symbol, 1 / 100)))
    question = utils.string('chemicalElementBySymbol').f(symbol=symbol)
    return question, collector.answers


@question('science', ['science/chemicalElements'])
def symbolByChemicalElement(els):
    name, symbol = els.sample(1).iloc[0]
    collector = utils.Collector(symbol)
    collector.add(els.symbol, weights=els.symbol.map(_similarityMap(name, 1 / 100)))
    question = utils.string('symbolByChemicalElement').f(element=name)
    return question, collector.answers
