
class Querier:

    def __init__(self, url):
        try:
            from SPARQLWrapper import SPARQLWrapper, JSON
            self._url = url
            agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
            self._client = SPARQLWrapper(url, agent=agent)
            self._client.setReturnFormat(JSON)
        except:
            raise QuerierError()

    @property
    def endpointUrl(self):
        return self._url

    def _buildResult(self, query, result):
        import pandas
        table = {}
        columns = result['head']['vars']
        rows = result['results']['bindings']
        for column in columns:
            data = [row[column]['value'] for row in rows]
            table[column] = data
        return pandas.DataFrame(data=table)

    def _query(self, query):
        try:
            self._client.setQuery(query)
            return self._client.queryAndConvert()
        except:
            raise QuerierError()

    def query(self, query):
        result = self._query(query)
        return self._buildResult(query, result)


def query(url, query):
    return Querier(url).query(query)


class QuerierError(Exception):
    pass

