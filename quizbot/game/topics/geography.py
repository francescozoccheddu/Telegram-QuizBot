from ..quiz import Topic, question, dependency, cachedDependency, answersCount
from ...utils import sparql, resources
import random

topic = Topic('geography')


@dependency
def config():
    return resources.json('topics/geography/config.json')


@cachedDependency
def countries():
    cfg = config()['countries']
    query = resources.text(cfg['queryFile'])
    listConverter = sparql.makeListConverter(cfg['listSeparator'])
    converters = {
        'continents': listConverter,
        'currencies': listConverter,
        'borders': listConverter,
        'cities': listConverter,
        'languages': listConverter,
        'area': float,
        'population': int,
        'populationDensity': float,
        'gdp': float,
    }
    return sparql.query(cfg['endpointUrl'], query, converters=converters)


@cachedDependency
def continents():
    cfg = config()['continents']
    query = resources.text(cfg['queryFile'])
    converters = {
        'hasCountries': sparql.boolConverter
    }
    return sparql.query(cfg['endpointUrl'], query, converters=converters)


@cachedDependency
def languages():
    cfg = config()['languages']
    query = resources.text(cfg['queryFile'])
    return sparql.query(cfg['endpointUrl'], query)


@cachedDependency
def currencies():
    cfg = config()['currencies']
    query = resources.text(cfg['queryFile'])
    return sparql.query(cfg['endpointUrl'], query)


def _countryWithSingleAttribute(key):
    c = countries.data
    c = c[c[key].apply(lambda l: len(l) == 1)].sample(1)
    return c.country.iloc[0], c[key].iloc[0][0]


def _answersByList(data, rightAnswer):
    d = data.sample(answersCount)
    d = d[d.iloc[:, 0] != rightAnswer].sample(answersCount - 1).iloc[:, 0]
    return [rightAnswer] + list(d)


@question(topic, dependencies=[countries])
def whichCapitalByCountry():
    pass


@question(topic, dependencies=[countries])
def whichCountryByCapital():
    res = countries.data.sample(answersCount)
    capital = res.capital.iloc[0]
    answers = list(res.country)
    return f'What country is {capital} the capital of?', answers


@question(topic, dependencies=[countries, languages])
def whichLanguageByCountry():
    country, language = _countryWithSingleAttribute('languages')
    answers = _answersByList(languages.data, language)
    return f'What is the official language of {country}?', answers


@question(topic, dependencies=[countries, currencies])
def whichCurrencyByCountry():
    country, currency = _countryWithSingleAttribute('currencies')
    answers = _answersByList(currencies.data, currency)
    return f'What is the official currency of {country}?', answers


@question(topic, dependencies=[countries, continents])
def whichContinentByCountry():
    country, continent = _countryWithSingleAttribute('continents')
    answers = _answersByList(continents.data, continent)
    return f'What is the continent of {country}?', answers


@question(topic, dependencies=[countries, continents])
def whichCountryInContinent():
    d = countries.data
    c = continents.data
    continent = c[c.hasCountries].sample(1).iloc[0][0]
    right = d[d.continents.apply(lambda cs: [continent] == cs)].sample(1)
    wrong = d[d.continents.apply(lambda cs: continent not in cs)].sample(answersCount - 1)
    answers = list(right.append(wrong).country)
    return f'Which country is in {continent}?', answers


@question(topic, dependencies=[countries, continents])
def whichCountryNotInContinent():
    d = countries.data
    c = continents.data
    continent = c[c.hasCountries].sample(1).iloc[0][0]
    right = d[d.continents.apply(lambda cs: continent not in cs)].sample(1)
    wrong = d[d.continents.apply(lambda cs: [continent] == cs)].sample(answersCount - 1)
    answers = list(right.append(wrong).country)
    return f'Which country is not in {continent}?', answers


@question(topic, dependencies=[countries])
def whichCountryByCity():
    pass


@question(topic, dependencies=[countries])
def whatPopulationByCountry():
    pass


@question(topic, dependencies=[countries])
def whichCountryByPopulation():
    pass


@question(topic, dependencies=[countries])
def whichCountryWithGreatestPopulation():
    pass


@question(topic, dependencies=[countries])
def whichCountryWithSmallestPopulation():
    pass


@question(topic, dependencies=[countries])
def whichCountryWithLargestArea():
    pass


@question(topic, dependencies=[countries])
def whichCountryWithSmallestArea():
    pass


@question(topic, dependencies=[countries])
def whichCountryIsRicher():
    pass


@question(topic, dependencies=[countries])
def whichCountryIsPoorer():
    pass


@question(topic, dependencies=[countries])
def whoSharesBorderWithCountry():
    pass


@question(topic, dependencies=[countries])
def whoDoesntShareBorderWithCountry():
    pass
