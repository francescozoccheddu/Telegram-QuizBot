import os
from ..utils import sparql, resources


def identityConverter(value):
    return value


def makeListConverter(delimiter=';', converter=identityConverter):
    def listConverter(value):
        return [converter(i) for i in value.split(delimiter)]
    return listConverter


def boolConverter(value):
    return value.strip().lower() == 'true'


converters = {
    'int': int,
    'float': float,
    'bool': boolConverter,
    'list': makeListConverter(';'),
}


def convert(data, converters):
    for key, converter in converters.items():
        data[key] = data[key].map(converter)


def queryByDescriptor(descriptor, relativePath=None):
    queryFile = descriptor['queryFile']
    if not os.path.isabs(queryFile):
        if relativePath is None:
            raise ValueError('Relative path required')
        queryFile = os.path.join(relativePath, queryFile)
    query = resources.text(queryFile)
    data = sparql.query(descriptor['endpoint'], query)
    if 'converters' in descriptor:
        convert(data, {k: converters[v] for k, v in descriptor['converters'].items()})
    return data


def queryByDescriptorDict(descriptors, filter=None, relativePath=None, progressCallback=None):
    keys = set(descriptors.keys())
    if filter is not None:
        keys = keys.intersection(set(filter))
    result = {}
    for i, key in enumerate(keys):
        result[key] = queryByDescriptor(descriptors[key], relativePath)
        if progressCallback is not None:
            progressCallback(i + 1, len(keys))
    return result


def queryByDescriptorResource(filename):
    return queryByDescriptor(resources.json(filename), os.path.dirname(filename))


def queryByDescriptorDictResource(filename, filter=None, progressCallback=None):
    return queryByDescriptorDict(resources.json(filename), filter, os.path.dirname(filename), progressCallback)
