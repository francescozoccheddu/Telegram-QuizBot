from ..quiz import question, answersCount
import random


def _countryWithSingleAttribute(countries, key):
    c = countries
    c = c[c[key].apply(lambda l: len(l) == 1)].sample(1)
    return c.country.iloc[0], c[key].iloc[0][0]


def _answersByList(data, rightAnswer):
    d = data.sample(answersCount())
    d = d[d.iloc[:, 0] != rightAnswer].sample(answersCount() - 1).iloc[:, 0]
    return [rightAnswer] + list(d)


@question("geography", datasets=["geography/countries"])
def whichCapitalByCountry(countries):
    pass


@question("geography", datasets=["geography/countries"])
def whichCountryByCapital(countries):
    res = countries.sample(answersCount())
    capital = res.capital.iloc[0]
    answers = list(res.country)
    return f'What country is {capital} the capital of?', answers


@question("geography", datasets=["geography/countries", "languages"])
def whichLanguageByCountry(countries, languages):
    country, language = _countryWithSingleAttribute(countries, 'languages')
    answers = _answersByList(languages, language)
    return f'What is the official language of {country}?', answers


@question("geography", datasets=["geography/countries", "currencies"])
def whichCurrencyByCountry(countries, currencies):
    country, currency = _countryWithSingleAttribute(countries, 'currencies')
    answers = _answersByList(currencies, currency)
    return f'What is the official currency of {country}?', answers


@question("geography", datasets=["geography/countries", "continents"])
def whichContinentByCountry(countries, continents):
    country, continent = _countryWithSingleAttribute(countries, 'continents')
    answers = _answersByList(continents, continent)
    return f'What is the continent of {country}?', answers


@question("geography", datasets=["geography/countries", "continents"])
def whichCountryInContinent(countries, continents):
    d = data
    c = continents
    continent = c[c.hasCountries].sample(1).iloc[0][0]
    right = d[d.continents.apply(lambda cs: [continent] == cs)].sample(1)
    wrong = d[d.continents.apply(lambda cs: continent not in cs)].sample(answersCount() - 1)
    answers = list(right.append(wrong).country)
    return f'Which country is in {continent}?', answers


@question("geography", datasets=["geography/countries", "continents"])
def whichCountryNotInContinent(countries, continents):
    d = data
    c = continents
    continent = c[c.hasCountries].sample(1).iloc[0][0]
    right = d[d.continents.apply(lambda cs: continent not in cs)].sample(1)
    wrong = d[d.continents.apply(lambda cs: [continent] == cs)].sample(answersCount() - 1)
    answers = list(right.append(wrong).country)
    return f'Which country is not in {continent}?', answers


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
