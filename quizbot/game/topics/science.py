from ..quiz import question, answersCount
import random


def _similarity(target, exclude, base):
    import textdistance
    return lambda v: 0 if v == exclude else textdistance.prefix.similarity(v, target) + base


@question('science', 0, ['science/chemicalElements'])
def whichChemicalElementBySymbol(els):
    name, symbol = els.sample(1).iloc[0]
    weights = els.name.map(_similarity(symbol, name, 1/100))
    wrongNames = els.name.sample(answersCount() - 1, weights=weights)
    return f'What chemical element has symbol {symbol}?', (name, *wrongNames)


@question('science', 0, ['science/chemicalElements'])
def whichSymbolByChemicalElement(els):
    name, symbol = els.sample(1).iloc[0]
    weights = els.symbol.map(_similarity(symbol, name, 1/100))
    wrongSymbols = els.symbol.sample(answersCount() - 1, weights=weights)
    return f'What is the symbol of {name}?', (symbol, *wrongSymbols)
