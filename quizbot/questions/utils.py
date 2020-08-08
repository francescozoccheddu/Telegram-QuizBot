from .questions import answersCount
from collections.abc import Iterable

_strings = None


def _loadStrings():
    global _strings
    if _strings is None:
        from ..utils import strings
        _strings = strings.fromResource('strings/questions.json')


def _around(right, rrange, min=None, max=None):
    if min is not None and max is not None:
        raise ValueError('Cannot use both constraints')
    import random
    fract = any(isinstance(r, float) for r in rrange)
    randf = random.randrange if fract else random.randint
    last, wrong = 0, []
    for _ in range(answersCount() - 1):
        last += randf(*rrange)
        y = random.choice((-last, last)) + right
        if max is not None and y > max:
            y = right - last
        if min is not None and y < min:
            y = right + last
        wrong.append(y)
    return (right, *wrong)


def string(key):
    _loadStrings()
    return _strings[key]


def dropDigits(value, digits):
    if value == 0:
        return 0
    import math
    actual = int(math.log10(abs(value))) + 1
    div = 10 ** max(actual - digits, 0)
    return int(round(abs(value) / div)) * div


def years(right, rrange=(7, 13)):
    import datetime
    import random
    now = datetime.datetime.now().year
    return _around(right, rrange, max=now)


def farSample(s, distanceMap=None):
    sample = s.sample(1)
    if distanceMap is None:
        def distanceMap(d): return d
    for _ in range(answersCount() - 1):
        w = s.apply(lambda v: min(distanceMap(abs(v - o)) for o in sample))
        sample = sample.append(s.sample(1, weights=w))
    return s[sample.index]


def format(right, wrong, format):
    import pandas
    answers = pandas.concat([right, wrong])
    keys = tuple(answers.columns)
    return tuple(answers.apply(lambda row: format.format(**dict(zip(keys, row))), axis=1))


class Collector:

    def __init__(self, right):
        self._wrong = set()
        if isinstance(right, Iterable) and not isinstance(right, str):
            self._right = set(right)
        else:
            self._right = {right}

    @property
    def full(self):
        return len(self._wrong) == answersCount() - 1

    @property
    def answers(self):
        import random
        return (random.choice(list(self._right)), *self._wrong)

    def addIterable(self, samples, mapping=lambda v: v, weights=None, globalWeights=True):
        if not self.full:
            if weights is not None and not globalWeights:
                if isinstance(weights, Iterable):
                    def w(i, s): return weights[i]
                if isinstance(weights, dict):
                    def w(i, s): return weights[s]
                elif callable(weights):
                    w = weights
                else:
                    raise TypeError('Unexpected non-global weights type')
            else:
                def w(i, s): return None
            for i, s in enumerate(samples):
                if self.add(mapping(s), weights=w(i, s)):
                    break
        return self.full

    def add(self, sample, weights=None):
        if not self.full:
            try:
                sampleset = set(sample)
            except TypeError:
                sampleset = {sample}
            sampleset -= self._right
            sampleset -= self._wrong
            sampleset = list(sampleset)
            k = min(len(sampleset), answersCount() - 1 - len(self._wrong))
            if weights is None:
                import random
                self._wrong.update(random.sample(sampleset, k=k))
            else:
                if isinstance(weights, Iterable):
                    weights = dict(zip(sample, weights))
                if isinstance(weights, dict):
                    w = [weights[s] for s in sampleset]
                elif callable(weights):
                    w = [weights(s) for s in sampleset]
                else:
                    raise TypeError('Unexpected weights type')
                import pandas
                sampleset = pandas.Series(sampleset)
                self._wrong.update(sampleset.sample(n=k, weights=w))
        return self.full
