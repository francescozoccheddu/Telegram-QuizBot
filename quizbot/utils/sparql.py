

# Querying


class Querier:

    def __init__(self, url, prefixes=[]):
        try:
            from SPARQLWrapper import SPARQLWrapper2
            self._url = url
            self._client = SPARQLWrapper2(url)
            self._prefixes = prefixes
            self._prefix = prefix(*prefixes)
        except:
            raise QuerierError()

    @property
    def endpointUrl(self):
        return self._url

    @property
    def prefixes(self):
        return self._prefixes

    @staticmethod
    def _defaultConverter(value):
        return value

    def _buildResult(self, query, result, converters={}):
        import pandas
        table = {}
        for column in result.variables:
            converter = converters.get(column, identityConverter)
            data = [converter(row[column].value) for row in result.bindings]
            table[column] = data
        return pandas.DataFrame(data=table)

    def _query(self, query):
        try:
            self._client.setQuery(query)
            return self._client.query()
        except:
            raise QuerierError()

    def query(self, query, converters={}):
        query = self._prefix + '\n' + query
        result = self._query(query)
        return self._buildResult(query, result, converters)


def query(url, query, prefixes=[], converters={}):
    return Querier(url, prefixes).query(query, converters)


class QuerierError(Exception):
    pass


# Language helpers


def filterLanguage(variable, language='EN'):
    return f'FILTER langMatches(lang(?{variable}), "EN").'


def label(variable, outputVariable, rdfsPrefix='rdfs', language='EN'):
    return f'?{variable} {rdfsPrefix}:label ?{outputVariable}. {filterLanguage(outputVariable, language)}'


def randomSample(count, randomPoolSize=2 ** 16):
    import random
    return f'ORDER BY RAND({random.randint(0, randomPoolSize)}) LIMIT {count}'


def prefix(*nameUrlPairs):
    return '\n'.join(map(lambda p: f'PREFIX {p[0]}: <{p[1]}>', nameUrlPairs))


# Utility converters

def identityConverter(value):
    return value

def makeListConverter(delimiter=';', converter=identityConverter):
    def listConverter(value):
        return [converter(i) for i in value.split(delimiter)]
    return listConverter
