from ..questions import question, answersCount
import random
from .. import utils


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


def _humanizePopulation(population):
    import humanize
    return humanize.intword(utils.dropDigits(population, 3))


def _farSampleBy(countries, by, exponent):
    by = countries[by].apply(lambda v: utils.dropDigits(v, 2))
    return countries.iloc[utils.farSample(by, lambda d: d**exponent).index]


@question("geography", ["geography/countries"])
def whichCapitalByCountry(cts):
    right = cts.sample(1).iloc[0]
    country, capital, cities = right[['country', 'capital', 'cities']]
    collector = utils.Collector(capital)
    collector.add(cities)
    if not collector.full:
        collector.addIterable(_countriesBySimilarity(cts, right).cities)
    return f'What is the capital of {country}?', collector.answers


@question("geography", ["geography/countries"])
def whichCountryByCapital(cts):
    right = cts.sample(1).iloc[0]
    country, capital = right[['country', 'capital']]
    collector = utils.Collector(country)
    ctss = _countriesBySimilarity(cts, right)
    collector.add(ctss[ctss.capital != capital].country)
    return f'What country is {capital} the capital of?', collector.answers


@question("geography", ["geography/countries", "geography/languages"])
def whichLanguageByCountry(cts, lgs):
    country, languages = cts.sample(1).iloc[0][['country', 'languages']]
    collector = utils.Collector(languages)
    collector.add(lgs.language)
    return f'What is the official language of {country}?', collector.answers


@question("geography", ["geography/countries", "geography/currencies"])
def whichCurrencyByCountry(cts, ccs):
    country, currencies = cts.sample(1).iloc[0][['country', 'currencies']]
    collector = utils.Collector(currencies)
    collector.add(ccs.currency)
    return f'What is the official currency of {country}?', collector.answers


@question("geography", ["geography/countries", "geography/continents"])
def whichContinentByCountry(cts, cns):
    country, continents = cts.sample(1).iloc[0][['country', 'continents']]
    collector = utils.Collector(continents)
    collector.add(cns.continent)
    return f'What is the continent of {country}?', collector.answers


@question("geography", ["geography/countries", "geography/continents"])
def whichCountryInContinent(cts, cns):
    continent = cns[cns.hasCountries].sample(1).iloc[0].continent
    country = cts[cts.continents.apply(lambda c: c == [continent])].sample(1).iloc[0].country
    collector = utils.Collector(country)
    collector.add(cts.country[cts.continents.apply(lambda c: continent not in c)])
    return f'What country is in {continent}?', collector.answers


@question("geography", ["geography/countries", "geography/continents"])
def whichCountryNotInContinent(cts, cns):
    continent = cns[cns.hasCountries].sample(1).iloc[0].continent
    country = cts[cts.continents.apply(lambda c: continent not in c)].sample(1).iloc[0].country
    collector = utils.Collector(country)
    collector.add(cts.country[cts.continents.apply(lambda c: continent in c)])
    return f'What country is not part of {continent}?', collector.answers


@question("geography", ["geography/countries"])
def whichCountryByCity(cts):
    right = cts.sample(1).iloc[0]
    country, cities = right[['country', 'cities']]
    collector = utils.Collector(country)
    collector.add(_countriesBySimilarity(cts, right).country)
    return f'What country is {random.choice(cities)} in?', collector.answers


@question("geography", ["geography/countries"])
def whichCountryByPopulation(cts):
    sample = _farSampleBy(cts, 'population', 0.1)
    population = _humanizePopulation(sample.iloc[0].population)
    return f'What country has population {population}?', tuple(sample.country)


@question("geography", ["geography/countries"])
def whichCountryWithGreatestPopulation(cts):
    sample = _farSampleBy(cts, 'population', 0.1).sort_values('population', ascending=False)
    return f'What country is more populated?', tuple(sample.country)


@question("geography", ["geography/countries"])
def whichCountryWithSmallestPopulation(cts):
    sample = _farSampleBy(cts, 'population', 0.1).sort_values('population', ascending=True)
    return f'What country is less populated?', tuple(sample.country)


@question("geography", ["geography/countries"])
def whichCountryWithLargestArea(cts):
    sample = _farSampleBy(cts, 'area', 0.1).sort_values('area', ascending=False)
    return f'What country is largest?', tuple(sample.country)


@question("geography", ["geography/countries"])
def whichCountryWithSmallestArea(cts):
    sample = _farSampleBy(cts, 'area', 0.1).sort_values('area', ascending=True)
    return f'What country is smallest?', tuple(sample.country)


@question("geography", ["geography/countries"])
def whichCountryIsRicher(cts):
    sample = _farSampleBy(cts, 'gdp', 0.1).sort_values('gdp', ascending=False)
    return f'What country is richer?', tuple(sample.country)


@question("geography", ["geography/countries"])
def whichCountryIsPoorer(cts):
    sample = _farSampleBy(cts, 'gdp', 0.1).sort_values('gdp', ascending=True)
    return f'What country is poorer?', tuple(sample.country)


@question("geography", ["geography/countries"])
def whoSharesBorderWithCountry(cts):
    right = cts.sample(1).iloc[0]
    country, borders = right[['country', 'borders']]
    cts = _countriesBySimilarity(cts, right)
    wrong = cts[~cts.country.isin(borders + [country])].sample(answersCount()-1).country
    return f'Which country shares a land or maritime border with {country}?', (random.choice(borders), *wrong)
