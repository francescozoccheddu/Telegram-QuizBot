from ..quiz import Topic, question, dependency, cachedDependency, answerCount
from ...utils import range, sparql, resources

topic = Topic('geography')


@dependency
def config():
    return resources.json('topics/geography/config.json')


@cachedDependency
def countries():
    cfg = config()
    query = resources.text(cfg['queryFiles']['countries'])
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
        'hdi': float,
    }
    return sparql.query(cfg['endpointUrl'], query, converters=converters)


@cachedDependency
def continents():
    cfg = config()
    query = resources.text(cfg['queryFiles']['continents'])
    return sparql.query(cfg['endpointUrl'], query)


@cachedDependency
def languages():
    cfg = config()
    query = resources.text(cfg['queryFiles']['languages'])
    return sparql.query(cfg['endpointUrl'], query)


@cachedDependency
def currencies():
    cfg = config()
    query = resources.text(cfg['queryFiles']['currencies'])
    return sparql.query(cfg['endpointUrl'], query)


def _countriesByDifficulty(difficulty):
    d = countries.data
    if difficulty is None:
        return d
    hdiMaxRange = range.Range(0.7, 1)
    hdiMinRange = range.Range(0, 0.7)
    hdiMin = hdiMinRange.lerp(1 - difficulty)
    hdiMax = hdiMaxRange.lerp(1 - difficulty)
    return d[(hdiMin <= d.hdi) & (d.hdi <= hdiMax)]


def _countryWithSingleAttribute(difficulty, key):
    c = _countriesByDifficulty(difficulty)
    c = c[c[key].apply(lambda l: len(l) == 1)].sample(1)
    return c.country.iloc[0], c[key].iloc[0][0]


def _answersByList(data, rightAnswer):
    d = data.sample(answerCount)
    d = d[d.iloc[:, 0] != rightAnswer].sample(answerCount - 1).iloc[:, 0]
    return [rightAnswer] + list(d)


@question(topic, dependencies=[countries])
def whichCapitalByCountry(difficulty):
    res = _countriesByDifficulty(difficulty).sample(answerCount)
    country = res.country.iloc[0]
    answers = list(res.capital)
    return f'What is the capital of {country}?', answers


@question(topic, dependencies=[countries])
def whichCountryByCapital(difficulty):
    res = _countriesByDifficulty(difficulty).sample(answerCount)
    capital = res.capital.iloc[0]
    answers = list(res.country)
    return f'What country is {capital} the capital of?', answers


@question(topic, dependencies=[countries, languages])
def whichLanguageByCountry(difficulty):
    country, language = _countryWithSingleAttribute(difficulty, 'languages')
    answers = _answersByList(languages.data, language)
    return f'What is the official language of {country}?', answers


@question(topic, dependencies=[countries, currencies])
def whichCurrencyByCountry(difficulty):
    country, currency = _countryWithSingleAttribute(difficulty, 'currencies')
    answers = _answersByList(currencies.data, currency)
    return f'What is the official currency of {country}?', answers


@question(topic, dependencies=[countries, continents])
def whichContinentByCountry(difficulty):
    country, continent = _countryWithSingleAttribute(difficulty, 'continents')
    answers = _answersByList(continents.data, continent)
    return f'What is the continent of {country}?', answers


@question(topic, dependencies=[countries])
def whichCountryNotInContinent(difficulty):
    pass


@question(topic, dependencies=[countries])
def whatPopulationByCountry(difficulty):
    pass


@question(topic, dependencies=[countries])
def whichCountryByPopulation(difficulty):
    pass


@question(topic, dependencies=[countries])
def whichCountryWithGreatestPopulation(difficulty):
    pass


@question(topic, dependencies=[countries])
def whichCountryWithSmallestPopulation(difficulty):
    pass


@question(topic, dependencies=[countries])
def whichCountryWithLargestArea(difficulty):
    pass


@question(topic, dependencies=[countries])
def whichCountryWithSmallestArea(difficulty):
    pass


@question(topic, dependencies=[countries])
def whichCountryIsRicher(difficulty):
    pass


@question(topic, dependencies=[countries])
def whichCountryIsPoorer(difficulty):
    pass
