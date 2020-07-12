
def contains(range, x, minInclusive=True, maxInclusive=True):
    min, max = range
    return (x >= min if minInclusive else x > min) and (x <= max if maxInclusive else x < max)


def lerp(range, progress, clamp=False):
    min, max = range
    if clamp:
        progress = clamp(0, 1, progress)
    return max * progress + min * (1 - progress)


def getProgress(range, x):
    min, max = range
    return (x - min) / (max - min) if max != min else 0


def clamp(range, x):
    min, max = range
    return max if x > max else min if x < min else x


class Range:

    @staticmethod
    def ensure(*args):
        if len(args) == 1:
            arg = args[0]
            if isinstance(arg, Range):
                return arg
            elif isinstance(arg, (tuple, list)) and len(arg) == 2:
                return Range(arg[0], arg[1])
        elif len(args) == 2:
            return Range(args[0], args[1])
        raise TypeError('Expected range')

    def __init__(self, min, max):
        if not isinstance(min, (int, float)) or not isinstance(max, (int, float)):
            raise TypeError()
        if min > max:
            raise ValueError()
        self._min = min
        self._max = max

    @property
    def min(self):
        return self._min

    @property
    def max(self):
        return self._max

    @property
    def range(self):
        return self._max - self._min

    @property
    def tuple(self):
        return (self._min, self._max)

    def __iter__(self):
        return iter(self.tuple)

    def contains(self, x, minInclusive=True, maxInclusive=True):
        return contains(self.tuple, x, minInclusive, maxInclusive)

    def lerp(self, progress, clamp=False):
        return lerp(self.tuple, progress, clamp)

    def getProgress(self, x):
        return getProgress(self, x)

    def clamp(self, x):
        return clamp(self.tuple, x)

    def __repr__(self):
        return f'{self.__class__.__name__}{(self._min,self._max)}'