
_converters = {
    'int': int,
    'float': float,
    'bool': lambda v: v.strip().lower() == 'true',
    'list': lambda v: v.split(';')
}


class Dataset:

    def __init__(self, descriptor):
        if not {'endpoint', 'query'} <= descriptor.keys() <= {'endpoint', 'query', 'converters'}:
            raise ValueError('Bad signature keys')
        if descriptor.get('converters', None) is None:
            descriptor['converters'] = {}
        if not (isinstance(descriptor['endpoint'], str) and isinstance(descriptor['query'], str) and isinstance(descriptor['converters'], dict)):
            raise TypeError('Bad signature types')
        for v in descriptor['converters'].values():
            if v not in _converters:
                raise ValueError(f'Unknown converter "{str(v)}"')
        descriptor['endpoint'] = descriptor['endpoint'].strip()
        descriptor['query'] = descriptor['query'].strip()
        self._descriptor = descriptor
        self._data = None

    @property
    def descriptor(self):
        return self._descriptor

    @property
    def isReady(self):
        return self._data is not None

    @property
    def data(self):
        if not self.isReady:
            raise Exception('Not ready')
        return self._data

    def ready(self):
        if not self.isReady:
            from ..utils import sparql
            data = sparql.query(self._descriptor['endpoint'], self._descriptor['query'])
            for column, converterKey in self._descriptor['converters'].items():
                data[column] = data[column].map(_converters[converterKey])
            self._data = data

    def __getstate__(self):
        return (self._descriptor, self._data)

    def __setstate__(self, state):
        self._descriptor, self._data = state


def _resolve(data, keyProvider, tree):
    result = {}
    if isinstance(data, dict):
        if 'endpoint' in data or 'query' in data:
            key = keyProvider(tree)
            result[key] = Dataset(data)
        else:
            for k, v in data.items():
                result.update(_resolve(v, keyProvider, (*tree, k)))
    elif isinstance(data, list):
        for i, v in enumerate(data):
            result.update(_resolve(v, keyProvider, (*tree, i)))
    else:
        raise TypeError('Expected dataset descriptor, dict or list')
    return result


def resolve(data, keyProvider):
    return _resolve(data, keyProvider, tuple())


def mergeFromCache(datasetMap, cacheFilename):
    from ..utils import data
    cached, cache = data.loadCache(cacheFilename)
    if cached:
        class DescriptorKey:

            def __init__(self, descriptor):
                self._descriptor = descriptor

            def __hash__(self):
                return hash((self._descriptor['endpoint'], self._descriptor['query']))

            def __eq__(self, other):
                return self._descriptor == other._descriptor

        targets = {DescriptorKey(d.descriptor): d for d in datasetMap.values()}
        for d in cache:
            target = targets.get(DescriptorKey(d.descriptor), None)
            if target is not None:
                target._data = d._data


def fromResource(filename, keyProvider, cacheFilename=None):
    from ..utils import resources
    datasetMap = resolve(resources.json(filename), keyProvider)
    if cacheFilename:
        mergeFromCache(datasetMap, cacheFilename)
    return datasetMap


def cache(datasetMap, filename):
    from ..utils import data
    return data.storeCache(filename, [d for d in datasetMap.values() if d.isReady])
