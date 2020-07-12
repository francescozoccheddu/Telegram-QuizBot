from SPARQLWrapper import SPARQLWrapper2
import random


class Querier:

    def __init__(self, url, prefixes=[]):
        try:
            self._client = SPARQLWrapper2(url)
            self._prefix = prefix(*prefixes)
        except:
            raise QuerierError()

    @staticmethod
    def defaultConverter(result):
        return result.value

    @staticmethod
    def _convertRow(row, converters={}):
        res = {}
        for key, value in row.items():
            converter = converters.get(key, Querier.defaultConverter)
            res[key] = converter(value)
        return Row(res)

    @staticmethod
    def _convertResult(result, converters={}):
        return [Querier._convertRow(row) for row in result.bindings]

    def _query(self, query):
        try:
            self._client.setQuery(self._prefix + '\n' + query)
            return self._client.query()
        except:
            raise QuerierError()

    def query(self, query, converters=None):
        result = self._query(query)
        return self._convertResult(result, converters)


class QuerierError(Exception):
    pass


class Row:

    def __init__(self, dict):
        self._dict = dict

    def __getitem__(self, key):
        return self._dict[key]

    def __getattr__(self, key):
        return self[key]

    @property
    def dict(self):
        return self._dict


def filterLanguage(variable, language='EN'):
    return f'FILTER langMatches(lang(?{variable}), "EN").'


def label(variable, outputVariable, rdfsPrefix='rdfs', language='EN'):
    return f'?{variable} {rdfsPrefix}:label ?{outputVariable}. {filterLanguage(outputVariable, language)}'


def randomSample(count, randomPoolSize=2**16):
    return f'ORDER BY RAND({random.randint(0, randomPoolSize)}) LIMIT {count}'


def prefix(*nameUrlPairs):
    return '\n'.join(map(lambda p: f'PREFIX {p[0]}: <{p[1]}>', nameUrlPairs))


def query(url, query, prefixes=[]):
    return Querier(url, prefixes).query(query)


dbpediaEndpointURL = 'https://dbpedia.org/sparql'
rdfsPrefix = ('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
dbpediaPrefixes = [('dbo', 'http://dbpedia.org/ontology/'), ('dbp', 'http://dbpedia.org/property/')]
