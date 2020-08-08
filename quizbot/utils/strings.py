
def fromResource(filename):
    from . import resources
    return fromDict(resources.json(filename))


_singularPrefix = '_Singular'
_pluralPrefix = '_Plural'


def fromDict(data):
    if isinstance(data, str):
        return String(data)
    if isinstance(data, list):
        return [fromDict(i) for i in data]
    if isinstance(data, dict):
        newDict = {}
        for k, v in data.items():
            if isinstance(v, str):
                if k.endswith(_singularPrefix):
                    key = k[:-len(_singularPrefix)]
                    plural = data.get(key + _pluralPrefix, None)
                    if isinstance(plural, (str, type(None))):
                        newDict[key] = String(v, plural)
                        continue
                elif k.endswith(_pluralPrefix):
                    key = k[:-len(_pluralPrefix)]
                    singular = data.get(key + _singularPrefix, None)
                    if singular is None:
                        newDict[key] = String(singular, v)
                    continue
            newDict[k] = fromDict(v)
        return newDict
    else:
        return data


class String:

    def __init__(self, singular, plural=None):
        self._singular = singular
        self._plural = plural

    def f(self, **kwargs):
        return self._singular.format(**kwargs)

    def p(self, isPlural, **kwargs):
        singular = self._singular if self._singular is not None else self._plural
        plural = self._plural if self._plural is not None else self._singular
        if isinstance(isPlural, (int, float)):
            isPlural = isPlural != 1
        text = plural if isPlural else singular
        return text.format(**kwargs)

    def __str__(self):
        return self._singular if self._singular is not None else self._plural
