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
def capitalByCountry(cts):
    right = cts.sample(1).iloc[0]
    country, capital, cities = right[['country', 'capital', 'cities']]
    collector = utils.Collector(capital)
    collector.add(cities)
    if not collector.full:
        collector.addIterable(_countriesBySimilarity(cts, right).cities)
    question = utils.string('capitalByCountry').f( country=country)
    return question, collector.answers


@question("geography", ["geography/countries"])
def countryByCapital(cts):
    right = cts.sample(1).iloc[0]
    country, capital = right[['country', 'capital']]
    collector = utils.Collector(country)
    ctss = _countriesBySimilarity(cts, right)
    collector.add(ctss[ctss.capital != capital].country)
    question = utils.string('countryByCapital').f( capital=capital)
    return question, collector.answers


@question("geography", ["geography/countries", "geography/languages"])
def languageByCountry(cts, lgs):
    country, languages = cts.sample(1).iloc[0][['country', 'languages']]
    collector = utils.Collector(languages)
    collector.add(lgs.language)
    question = utils.string('languageByCountry').f( country=country)
    return question, collector.answers


@question("geography", ["geography/countries", "geography/currencies"])
def currencyByCountry(cts, ccs):
    country, currencies = cts.sample(1).iloc[0][['country', 'currencies']]
    collector = utils.Collector(currencies)
    collector.add(ccs.currency)
    question = utils.string('currencyByCountry').f( country=country)
    return question, collector.answers


@question("geography", ["geography/countries", "geography/continents"])
def continentByCountry(cts, cns):
    country, continents = cts.sample(1).iloc[0][['country', 'continents']]
    collector = utils.Collector(continents)
    collector.add(cns.continent)
    question = utils.string('continentByCountry').f( country=country)
    return question, collector.answers


@question("geography", ["geography/countries", "geography/continents"])
def countryByContinent(cts, cns):
    continent = cns[cns.hasCountries].sample(1).iloc[0].continent
    country = cts[cts.continents.apply(lambda c: c == [continent])].sample(1).iloc[0].country
    collector = utils.Collector(country)
    collector.add(cts.country[cts.continents.apply(lambda c: continent not in c)])
    question = utils.string('countryByContinent').f( continent=continent)
    return question, collector.answers


@question("geography", ["geography/countries", "geography/continents"])
def countryNotInContinent(cts, cns):
    continent = cns[cns.hasCountries].sample(1).iloc[0].continent
    country = cts[cts.continents.apply(lambda c: continent not in c)].sample(1).iloc[0].country
    collector = utils.Collector(country)
    collector.add(cts.country[cts.continents.apply(lambda c: continent in c)])
    question = utils.string('countryNotInContinent').f( continent=continent)
    return question, collector.answers


@question("geography", ["geography/countries"])
def countryByCity(cts):
    right = cts.sample(1).iloc[0]
    country, cities = right[['country', 'cities']]
    collector = utils.Collector(country)
    collector.add(_countriesBySimilarity(cts, right).country)
    question = utils.string('countryByCity').f( city=random.choice(cities))
    return question, collector.answers


@question("geography", ["geography/countries"])
def countryByPopulation(cts):
    sample = _farSampleBy(cts, 'population', 0.1)
    population = _humanizePopulation(sample.iloc[0].population)
    question = utils.string('countryByPopulation').f( population=population)
    return question, tuple(sample.country)


@question("geography", ["geography/countries"])
def mostPopulatedCountry(cts):
    sample = _farSampleBy(cts, 'population', 0.1).sort_values('population', ascending=False)
    question = utils.string('mostPopulatedCountry').f()
    return question, tuple(sample.country)


@question("geography", ["geography/countries"])
def leastPopulatedCountry(cts):
    sample = _farSampleBy(cts, 'population', 0.1).sort_values('population', ascending=True)
    question = utils.string('leastPopulatedCountry').f()
    return question, tuple(sample.country)


@question("geography", ["geography/countries"])
def largestCountry(cts):
    sample = _farSampleBy(cts, 'area', 0.1).sort_values('area', ascending=False)
    question = utils.string('largestCountry').f()
    return question, tuple(sample.country)


@question("geography", ["geography/countries"])
def smallestCountry(cts):
    sample = _farSampleBy(cts, 'area', 0.1).sort_values('area', ascending=True)
    question = utils.string('smallestCountry').f()
    return question, tuple(sample.country)


@question("geography", ["geography/countries"])
def richestCountry(cts):
    sample = _farSampleBy(cts, 'gdp', 0.1).sort_values('gdp', ascending=False)
    question = utils.string('richestCountry').f()
    return question, tuple(sample.country)


@question("geography", ["geography/countries"])
def poorestCountry(cts):
    sample = _farSampleBy(cts, 'gdp', 0.1).sort_values('gdp', ascending=True)
    question = utils.string('poorestCountry').f()
    return question, tuple(sample.country)


@question("geography", ["geography/countries"])
def countryByNeighbor(cts):
    right = cts.sample(1).iloc[0]
    country, borders = right[['country', 'borders']]
    cts = _countriesBySimilarity(cts, right)
    wrong = cts[~cts.country.isin(borders + [country])].sample(answersCount() - 1).country
    question = utils.string('countryByNeighbor').f( country=country)
    return question, (random.choice(borders), *wrong)
