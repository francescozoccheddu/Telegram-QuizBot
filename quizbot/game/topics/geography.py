from ..quiz import Topic, question, dependency, cachedDependency, answersCount
from ...utils import autosparql, resources
import random

topic = Topic('geography')


@cachedDependency
def data():
    return autosparql.queryByDescriptorsResource('topics/geography/auto.json')


def _countryWithSingleAttribute(key):
    c = data.data['countries']
    c = c[c[key].apply(lambda l: len(l) == 1)].sample(1)
    return c.country.iloc[0], c[key].iloc[0][0]


def _answersByList(data, rightAnswer):
    d = data.sample(answersCount)
    d = d[d.iloc[:, 0] != rightAnswer].sample(answersCount - 1).iloc[:, 0]
    return [rightAnswer] + list(d)


@question(topic, dependencies=[data])
def whichCapitalByCountry():
    pass


@question(topic, dependencies=[data])
def whichCountryByCapital():
    res = data.data['countries'].sample(answersCount)
    capital = res.capital.iloc[0]
    answers = list(res.country)
    return f'What country is {capital} the capital of?', answers


@question(topic, dependencies=[data])
def whichLanguageByCountry():
    country, language = _countryWithSingleAttribute('languages')
    answers = _answersByList(data.data['languages'], language)
    return f'What is the official language of {country}?', answers


@question(topic, dependencies=[data])
def whichCurrencyByCountry():
    country, currency = _countryWithSingleAttribute('currencies')
    answers = _answersByList(data.data['currencies'], currency)
    return f'What is the official currency of {country}?', answers


@question(topic, dependencies=[data])
def whichContinentByCountry():
    country, continent = _countryWithSingleAttribute('continents')
    answers = _answersByList(data.data['continents'], continent)
    return f'What is the continent of {country}?', answers


@question(topic, dependencies=[data])
def whichCountryInContinent():
    d = data.data
    c = data.data['continents']
    continent = c[c.hasCountries].sample(1).iloc[0][0]
    right = d[d.continents.apply(lambda cs: [continent] == cs)].sample(1)
    wrong = d[d.continents.apply(lambda cs: continent not in cs)].sample(answersCount - 1)
    answers = list(right.append(wrong).country)
    return f'Which country is in {continent}?', answers


@question(topic, dependencies=[data])
def whichCountryNotInContinent():
    d = data.data
    c = data.data['continents']
    continent = c[c.hasCountries].sample(1).iloc[0][0]
    right = d[d.continents.apply(lambda cs: continent not in cs)].sample(1)
    wrong = d[d.continents.apply(lambda cs: [continent] == cs)].sample(answersCount - 1)
    answers = list(right.append(wrong).country)
    return f'Which country is not in {continent}?', answers


@question(topic, dependencies=[data])
def whichCountryByCity():
    pass


@question(topic, dependencies=[data])
def whatPopulationByCountry():
    pass


@question(topic, dependencies=[data])
def whichCountryByPopulation():
    pass


@question(topic, dependencies=[data])
def whichCountryWithGreatestPopulation():
    pass


@question(topic, dependencies=[data])
def whichCountryWithSmallestPopulation():
    pass


@question(topic, dependencies=[data])
def whichCountryWithLargestArea():
    pass


@question(topic, dependencies=[data])
def whichCountryWithSmallestArea():
    pass


@question(topic, dependencies=[data])
def whichCountryIsRicher():
    pass


@question(topic, dependencies=[data])
def whichCountryIsPoorer():
    pass


@question(topic, dependencies=[data])
def whoSharesBorderWithCountry():
    pass


@question(topic, dependencies=[data])
def whoDoesntShareBorderWithCountry():
    pass
