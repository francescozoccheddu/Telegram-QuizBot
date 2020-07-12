

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
    def _defaultConverter(result):
        return result.value

    @staticmethod
    def _buildRow(row, keys, converters={}):
        res = []
        for key in keys:
            converter = converters.get(key, Querier._defaultConverter)
            res.append(converter(row[key]))
        return tuple(res)

    def _buildResult(self, query, result, converters={}):
        data = tuple(Querier._buildRow(row, result.variables, converters) for row in result.bindings)
        return Result(self, query, result.variables, data)

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


def query(url, query, prefixes=[]):
    return Querier(url, prefixes).query(query)


# Result data structures


class QuerierError(Exception):
    pass


class Table:

    class IteratorWrapper:

        def __init__(self, table, horizontal):
            self._table = table
            self._horizontal = horizontal

        @property
        def isHorizontal(self):
            return self._horizontal

        @property
        def isVertical(self):
            return not self._horizontal

        @property
        def table(self):
            return self._table

        def __iter__(self):
            return Table.Iterator(self._table, self._horizontal)

    class Iterator:

        def __init__(self, table, horizontal):
            self._index = 0
            self._table = table
            self._horizontal = horizontal

        @property
        def isHorizontal(self):
            return self._horizontal

        @property
        def isVertical(self):
            return not self._horizontal

        @property
        def table(self):
            return self._table

        def _getRow(self, y):
            row = []
            for x in range(self._table._x, self._table._x + self._table._w):
                row.append(self._table._result._get(x, y))
            return tuple(row) if len(row) > 1 else row[0]

        def _getColumn(self, x):
            col = []
            for y in range(self._table._y, self._table._y + self._table._h):
                col.append(self._table._result._get(x, y))
            return tuple(col) if len(col) > 1 else col[0]

        def __next__(self):
            if self._horizontal:
                get = self._getColumn
                offs = self._table._x
                max = self._table._w
            else:
                get = self._getRow
                offs = self._table._y
                max = self._table._h
            if self._index < max:
                res = get(self._index + offs)
                self._index += 1
                return res
            else:
                raise StopIteration()

    def __init__(self, result, x, y, w, h):
        self._result = result
        self._x = x
        self._y = y
        self._w = w
        self._h = h

    @property
    def result(self):
        return self._result

    @property
    def isRow(self):
        return self._h == 1

    @property
    def isColumn(self):
        return self._w == 1

    @property
    def keys(self):
        return tuple(self._result._getKeyByColumn(x) for x in range(self._x, self._x + self._w))

    @property
    def key(self):
        if not self.isColumn:
            raise TypeError()
        return self._result._getKeyByColumn(self._x)

    @property
    def isLinear(self):
        return self.isRow or self.isColumn

    @property
    def width(self):
        return self._w

    @property
    def height(self):
        return self._h

    def iterHorizontal(self, zipKeys=False):
        iterator = Table.IteratorWrapper(self, True)
        if zipKeys:
            iterator = zip(self.keys, iterator)
        return iterator

    def iterVertical(self, zipKeys=False):
        iterator = Table.IteratorWrapper(self, False)
        if zipKeys:
            iterator = map(lambda row: dict(zip(self.keys, row)), iterator)
        return iterator

    def _sub(self, x, y, w, h):
        if w == h == 1:
            return self._result._get(x, y)
        else:
            return Table(self._result, x, y, w, h)

    def __getitem__(self, key):
        if isinstance(key, str):
            x = self._result._getColumnByKey(key)
            if not self._x <= x < self._x + self._w:
                raise KeyError()
            return self._sub(x, self._y, 1, self._h)
        elif isinstance(key, int):
            return self._sub(self._x, self._y + (key % self._h), self._w, 1)
        raise TypeError()

    def __len__(self):
        if self.isRow:
            return self.width
        elif self.isColumn:
            return self.height
        else:
            raise TypeError()

    def __iter__(self):
        if self.isRow:
            return Table.Iterator(self, True)
        elif self.isColumn:
            return Table.Iterator(self, False)
        else:
            raise TypeError()

    def __str__(self):
        from tabulate import tabulate
        data = list(self.iterVertical())
        if self.isColumn:
            data = [[c] for c in data]
        return str(tabulate(data, headers=self.keys))


class Result:

    def __init__(self, querier, query, keys, data):
        self._querier = querier
        self._query = query
        self._keysDict = dict(zip(keys, range(0, len(keys))))
        self._keysList = keys
        self._data = data
        self._table = Table(self, 0, 0, len(keys), len(data))

    def _get(self, x, y):
        return self._data[y][x]

    def _getColumnByKey(self, key):
        return self._keysDict[key]

    def _getKeyByColumn(self, index):
        return self._keysList[index]

    @property
    def querier(self):
        return self._querier

    @property
    def query(self):
        return self._query

    @property
    def table(self):
        return self._table


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


# Utility constants


dbpediaEndpointURL = 'https://dbpedia.org/sparql'
rdfsPrefix = ('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
dbpediaPrefixes = [('dbo', 'http://dbpedia.org/ontology/'), ('dbp', 'http://dbpedia.org/property/')]
