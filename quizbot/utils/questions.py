from ..game.quiz import answersCount
from collections.abc import Iterable


def years(right):
    import datetime
    import random
    now = datetime.datetime.now().year
    last, wrong = 0, []
    for i in range(answersCount() - 1):
        last += random.randint(7, 13)
        y = random.choice((-last, last)) + right
        if y > now:
            y = right - last
        wrong.append(y)
    return (right, *wrong)


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
                from numpy import random
                tot = sum(w)
                if tot != 0:
                    for i, v in enumerate(w):
                        w[i] = v / tot
                self._wrong.update(random.choice(sampleset, k, p=w, replace=False))
        return self.full
