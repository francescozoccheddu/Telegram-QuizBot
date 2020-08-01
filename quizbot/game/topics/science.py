from ..quiz import question
from ...utils import questions
import random

def _similarity(a, b):
    from nltk.metrics.distance import jaro_winkler_similarity
    return jaro_winkler_similarity(a, b)

def _similarityMap(target, offset=0):
    return lambda v: _similarity(target, v) + offset


@question('science', 0, ['science/chemicalElements'])
def whichChemicalElementBySymbol(els):
    name, symbol = els.sample(1).iloc[0]
    collector = questions.Collector(name)
    collector.add(els.name, weights=els.name.map(_similarityMap(symbol, 1 / 100)))
    return f'What chemical element has symbol {symbol}?', collector.answers


@question('science', 0, ['science/chemicalElements'])
def whichSymbolByChemicalElement(els):
    name, symbol = els.sample(1).iloc[0]
    collector = questions.Collector(symbol)
    collector.add(els.symbol, weights=els.symbol.map(_similarityMap(name, 1 / 100)))
    return f'What is the symbol of {name}?', collector.answers
