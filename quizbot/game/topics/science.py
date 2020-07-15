from ..quiz import question, answersCount
import textdistance
import random


@question('science', 0, ['science/chemicalElements'])
def whichChemicalElementBySymbol(e):
    sample = e.sample(1)
    name, symbol = sample.iloc[0]
    e = e[~e.index.isin(sample.index)]
    sim = e.name.map(lambda n: textdistance.prefix.similarity(n, symbol))
    best = e.name[sim.nlargest(answersCount() - 1 + 2).sample(answersCount() - 1).index]
    return f'What chemical element has symbol {symbol}?', (name, *best)


@question('science', 0, ['science/chemicalElements'])
def whichSymbolByChemicalElement(e):
    sample = e.sample(1)
    name, symbol = sample.iloc[0]
    e = e[~e.index.isin(sample.index)]
    sim = e.symbol.map(lambda s: textdistance.prefix.similarity(s, name))
    best = e.symbol[sim.nlargest(answersCount() - 1 + 2).sample(answersCount() - 1).index]
    return f'What is the symbol of {name}?', (symbol, *best)
