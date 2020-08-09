
def fromResource(filename):
    from . import resources
    return fromDict(resources.json(filename))


_singularKey = 'singular'
_pluralKey = 'plural'


def fromDict(data):
    if isinstance(data, str):
        return String(data)
    if isinstance(data, list):
        return [fromDict(i) for i in data]
    if isinstance(data, dict):
        if len(data) > 0 and all(k in [_singularKey, _pluralKey] and isinstance(v, str) for k, v in data.items()):
            return String(data.get(_singularKey, None), data.get(_pluralKey, None))
        else:
            return {k: fromDict(v) for k, v in data.items()}
    else:
        return data


class String:

    def __init__(self, singular, plural=None):
        self._singular = singular
        self._plural = plural

    def f(self, **kwargs):
        return self.s.format(**kwargs)

    @property
    def s(self):
        return self._plural if self._singular is None else self._singular

    def p(self, isPlural, **kwargs):
        singular = self._singular if self._singular is not None else self._plural
        plural = self._plural if self._plural is not None else self._singular
        if isinstance(isPlural, (int, float)):
            isPlural = isPlural != 1
        text = plural if isPlural else singular
        return text.format(**kwargs)

    def __str__(self):
        return self._singular if self._singular is not None else self._plural
