from ..quiz import Topic, question, dependency, answerCount
from ...utils import range, sparql

topic = Topic('geography')


@dependency()
def config():
    from ...utils import resources
    return resources.json('geography.json')


@dependency([config])
def countries():
    from ...utils import resources
    cached, cache = resources.loadCache('topics/geography/countries')
    if cached:
        return cache
    else:
        cfg = config.data
        query = resources.text(cfg['queryFilename'])
        listConverter = sparql.makeListConverter(cfg['listSeparator'])
        converters = {
            'borders': listConverter,
            'continents': listConverter,
            'currencies': listConverter,
            'languages': listConverter,
            'area': float,
            'population': int,
            'populationDensity': float,
            'gdp': float,
            'hdi': float,
        }
        data = sparql.query(cfg['endpointUrl'], query, converters=converters)
        resources.storeCache('topics/geography/countries', data)
        return data


@dependency([config])
def continents():
    pass


@dependency([config])
def languages():
    pass


def _dataByDifficulty(difficulty):
    d = countries.data
    if difficulty is None:
        return d
    hdiMaxRange = range.Range(0.7, 1)
    hdiMinRange = range.Range(0, 0.7)
    hdiMin = hdiMinRange.lerp(1 - difficulty)
    hdiMax = hdiMaxRange.lerp(1 - difficulty)
    return d[(hdiMin <= d.hdi) & (d.hdi <= hdiMax)]


@question(topic, dependencies=[countries])
def whichCapitalByCountry(difficulty):
    res = _dataByDifficulty(difficulty).sample(answerCount)
    country = res.country.iloc[0]
    answers = list(res.capital)
    return f'What is the capital of {country}?', answers


@question(topic, dependencies=[countries])
def whichCountryByCapital(difficulty):
    res = _dataByDifficulty(difficulty).sample(answerCount)
    capital = res.capital.iloc[0]
    answers = list(res.country)
    return f'What country is {capital} the capital of?', answers


@question(topic, dependencies=[countries])
def whichLanguageByCountry(difficulty):
    pass


@question(topic, dependencies=[countries])
def whichCurrencyByCountry(difficulty):
    pass


@question(topic, dependencies=[countries])
def whichContinentByCountry(difficulty):
    pass


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
