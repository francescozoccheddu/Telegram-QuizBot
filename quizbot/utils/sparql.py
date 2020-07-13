
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


def identityConverter(value):
    return value


def makeListConverter(delimiter=';', converter=identityConverter):
    def listConverter(value):
        return [converter(i) for i in value.split(delimiter)]
    return listConverter


def boolConverter(value):
    return value.strip().lower() == 'true'
