from ..quiz import Topic, question, dependency, answerCount
from ...utils import range, sparql

topic = Topic('geography')

_data = None


@dependency
def initialize():
    from ...utils import resources
    config = resources.json('geography.json')
    query = resources.text(config['queryFilename'])
    listConverter = sparql.makeListConverter(config['listSeparator'])
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
    global _data
    _data = sparql.query(config['endpointUrl'], query, converters=converters)


def _dataByDifficulty(difficulty):
    if difficulty is None:
        return _data
    hdiMinRange = range.Range(0.7, 0.9)
    hdiMaxRange = range.Range(0, 0.7)
    hdiMin = hdiMinRange.lerp(1 - difficulty)
    hdiMax = hdiMaxRange.lerp(1 - difficulty)
    return _data[hdiMin <= _data.hdi <= hdiMax]


@question(topic, dependencies=[initialize])
def whichCapitalByCountry(difficulty):
    pass


@question(topic, dependencies=[initialize])
def whichCountryByCapital(difficulty):
    pass


@question(topic, dependencies=[initialize])
def whichLanguageByCountry(difficulty):
    pass


@question(topic, dependencies=[initialize])
def whichCurrencyByCountry(difficulty):
    pass


@question(topic, dependencies=[initialize])
def whichContinentByCountry(difficulty):
    pass


@question(topic, dependencies=[initialize])
def whichCountryNotInContinent(difficulty):
    pass


@question(topic, dependencies=[initialize])
def whatPopulationByCountry(difficulty):
    pass


@question(topic, dependencies=[initialize])
def whichCountryByPopulation(difficulty):
    pass


@question(topic, dependencies=[initialize])
def whichCountryWithGreatestPopulation(difficulty):
    pass


@question(topic, dependencies=[initialize])
def whichCountryWithSmallestPopulation(difficulty):
    pass


@question(topic, dependencies=[initialize])
def whichCountryWithLargestArea(difficulty):
    pass


@question(topic, dependencies=[initialize])
def whichCountryWithSmallestArea(difficulty):
    pass


@question(topic, dependencies=[initialize])
def whichCountryIsRicher(difficulty):
    pass


@question(topic, dependencies=[initialize])
def whichCountryIsPoorer(difficulty):
    pass
