
class _Querier:

    def __init__(self, url):
        from SPARQLWrapper import SPARQLWrapper, JSON
        self._url = url
        agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        self._client = SPARQLWrapper(url, agent=agent)
        self._client.setReturnFormat(JSON)

    @property
    def endpointUrl(self):
        return self._url

    @staticmethod
    def _buildResult(query, result):
        import pandas
        table = {}
        columns = result['head']['vars']
        rows = result['results']['bindings']
        for column in columns:
            data = [row[column]['value'] for row in rows]
            table[column] = data
        return pandas.DataFrame(data=table)

    def _request(self, query):
        self._client.setQuery(query)
        return self._client.queryAndConvert()

    def query(self, query):
        result = self._request(query)
        return _Querier._buildResult(query, result)


def query(url, query):
    return _Querier(url).query(query)
