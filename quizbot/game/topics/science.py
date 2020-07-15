from ..quiz import question, answersCount
import textdistance
import random


@question('science', 0, ['science/chemicalElements'])
def whichChemicalElementBySymbol(e):
    sample = e.sample(1)
    name, symbol = sample.iloc[0]
    sim = e.name.map(lambda n: 0 if n == name else textdistance.prefix.similarity(n, symbol) + 1/100)
    best = e.name.sample(answersCount() - 1, weights=sim)
    return f'What chemical element has symbol {symbol}?', (name, *best)


@question('science', 0, ['science/chemicalElements'])
def whichSymbolByChemicalElement(e):
    sample = e.sample(1)
    name, symbol = sample.iloc[0]
    sim = e.symbol.map(lambda s: 0 if s == symbol else textdistance.prefix.similarity(s, name) + 1/100)
    best = e.symbol.sample(answersCount() - 1, weights=sim)
    return f'What is the symbol of {name}?', (symbol, *best)
