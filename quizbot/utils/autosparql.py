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


def queryByDescriptors(descriptors, filter=None, relativePath=None):
    return {k: queryByDescriptor(v, relativePath) for k, v in descriptors.items() if filter is None or k in filter}


def queryByDescriptorsResource(filename, filter=None):
    return queryByDescriptors(resources.json(filename), filter, os.path.dirname(filename))
