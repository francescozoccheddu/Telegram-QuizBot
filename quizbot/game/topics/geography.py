from ..quiz import question, answersCount
import random
from ...utils import questions


def _countrySimilarity(a, b):
    score = 0
    if b.country in a.borders:
        score += 2
    if len(set(a.continents) & set(b.continents)) > 0:
        score += 1
    return score


def _countriesBySimilarity(countries, country):
    import random
    def similarity(c): return _countrySimilarity(country, c) + random.random()
    return countries.iloc[countries.apply(similarity, axis=1).sort_values().index]


@question("geography", datasets=["geography/countries"])
def whichCapitalByCountry(cts):
    right = cts.sample(1).iloc[0]
    country, capital, cities = right[['country', 'capital', 'cities']]
    collector = questions.Collector(capital)
    collector.add(cities)
    if not collector.full:
        collector.addIterable(_countriesBySimilarity(cts, right).cities)
    return f'What is the capital of {country}?', collector.answers


@question("geography", datasets=["geography/countries"])
def whichCountryByCapital(cts):
    right = cts.sample(1).iloc[0]
    country, capital = right[['country', 'capital']]
    collector = questions.Collector(country)
    ctss = _countriesBySimilarity(cts, right)
    collector.add(ctss[ctss.capital != capital].country)
    return f'What country is {capital} the capital of?', collector.answers


@question("geography", datasets=["geography/countries", "geography/languages"])
def whichLanguageByCountry(cts, lgs):
    country, languages = cts.sample(1).iloc[0][['country', 'languages']]
    collector = questions.Collector(languages)
    collector.add(lgs.language)
    return f'What is the official language of {country}?', collector.answers


@question("geography", datasets=["geography/countries", "geography/currencies"])
def whichCurrencyByCountry(cts, ccs):
    country, currencies = cts.sample(1).iloc[0][['country', 'currencies']]
    collector = questions.Collector(currencies)
    collector.add(ccs.currency)
    return f'What is the official currency of {country}?', collector.answers


@question("geography", datasets=["geography/countries", "geography/continents"])
def whichContinentByCountry(cts, cns):
    country, continents = cts.sample(1).iloc[0][['country', 'continents']]
    collector = questions.Collector(continents)
    collector.add(cns.continent)
    return f'What is the continent of {country}?', collector.answers


@question("geography", datasets=["geography/countries", "geography/continents"])
def whichCountryInContinent(countries, continents):
    pass


@question("geography", datasets=["geography/countries", "geography/continents"])
def whichCountryNotInContinent(countries, continents):
    pass


@question("geography", datasets=["geography/countries"])
def whichCountryByCity(countries):
    pass


@question("geography", datasets=["geography/countries"])
def whatPopulationByCountry(countries):
    pass


@question("geography", datasets=["geography/countries"])
def whichCountryByPopulation(countries):
    pass


@question("geography", datasets=["geography/countries"])
def whichCountryWithGreatestPopulation(countries):
    pass


@question("geography", datasets=["geography/countries"])
def whichCountryWithSmallestPopulation(countries):
    pass


@question("geography", datasets=["geography/countries"])
def whichCountryWithLargestArea(countries):
    pass


@question("geography", datasets=["geography/countries"])
def whichCountryWithSmallestArea(countries):
    pass


@question("geography", datasets=["geography/countries"])
def whichCountryIsRicher(countries):
    pass


@question("geography", datasets=["geography/countries"])
def whichCountryIsPoorer(countries):
    pass


@question("geography", datasets=["geography/countries"])
def whoSharesBorderWithCountry(countries):
    pass


@question("geography", datasets=["geography/countries"])
def whoDoesntShareBorderWithCountry(countries):
    pass
