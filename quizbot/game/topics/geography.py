from ..quiz import Topic, question, answerCount
from ...utils import range, sparql, easing
import random

topic = Topic('geography')

_querier = sparql.Querier(sparql.dbpediaEndpointURL, [sparql.rdfsPrefix, *sparql.dbpediaPrefixes])
_filterCountries = f'?country a dbo:Country. FILTER NOT EXISTS {{?country dbo:dissolutionYear ?dissolutionYear}}.'


def query(query):
    return _querier.query(query)


def _filterCountriesByDifficulty(difficulty):
    if difficulty is None:
        return ''
    hdiMinRange = range.Range(0, 30)
    hdiMaxRange = range.Range(30, 190)
    hdiMinRank = hdiMinRange.lerp(difficulty)
    hdiMaxRank = hdiMaxRange.lerp(difficulty)
    return f'''
    ?country dbp:hdiRank ?hdiRank.
    FILTER(?hdiRank >= {hdiMinRank}).
    FILTER(?hdiRank <= {hdiMaxRank}).
    '''


@question(topic)
def whichCapitalByCountry(difficulty):
    res = query(f'''
    SELECT ?countryName ?capitalName
    WHERE {{
        {_filterCountries}
        ?country dbo:capital ?capital.
        {sparql.label('country', 'countryName')}
        {sparql.label('capital', 'capitalName')}
        {_filterCountriesByDifficulty(difficulty)}
    }} GROUP BY ?capital
    {sparql.randomSample(answerCount)}
    ''').table
    return f'What is the capital of {res["countryName"][0]}?', tuple(res['capitalName'])


@question(topic)
def whichCountryByCapital(difficulty):
    pass


@question(topic)
def whichLanguageByCountry(difficulty):
    pass


@question(topic)
def whichCurrencyByCountry(difficulty):
    pass


@question(topic)
def whichContinentByCountry(difficulty):
    pass


@question(topic)
def whichCountryNotInContinent(difficulty):
    pass


@question(topic)
def whatPopulationByCountry(difficulty):
    pass


@question(topic)
def whichCountryByPopulation(difficulty):
    pass


@question(topic)
def whichCountryWithGreatestPopulation(difficulty):
    pass


@question(topic)
def whichCountryWithSmallestPopulation(difficulty):
    pass


@question(topic)
def whichCountryWithLargestArea(difficulty):
    pass


@question(topic)
def whichCountryWithSmallestArea(difficulty):
    pass


@question(topic)
def whichCountryIsRicher(difficulty):
    pass


@question(topic)
def whichCountryIsPoorer(difficulty):
    pass
