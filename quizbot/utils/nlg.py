from .resources import LazyJson

_numbers = LazyJson('other/nlgNumbers.json')


def _invOrdinals():
    return dict(zip(_numbers.ordinals.values(), _numbers.ordinals.keys()))


def _invCardinals():
    return dict(zip(_numbers.cardinals.values(), _numbers.cardinals.keys()))


def ord(number):
    if isinstance(number, int) and 1 <= number <= len(_numbers.ordinal):
        return _numbers.ordinal[number - 1]
    else:
        return f'{number}{_numbers.ordinalSuffix}'


def card(number):
    if isinstance(number, int) and 0 <= number < len(_numbers.cardinal):
        return _numbers.cardinal[number]
    else:
        return f'{number}'


def invNum(word):
    word = word.strip().lower()
    if word.isdigit() or word.endswith(_numbers.ordinalSuffix) and word.replace(_numbers.ordinalSuffix, '').isdigit():
        return int(word)
    else:
        return {**_invOrdinals(), **_invCardinals()}.get(word, None)


def join(items, conjunction='and'):
    res = ''
    for i, v in enumerate(items):
        if i == 0:
            res += f'{v}'
        elif i == len(items) - 1:
            res += f' {conjunction} {v}'
        else:
            res += f', {v}'
    return res


def plur(number, plural='s', singular=''):
    if isinstance(number, (int, float)):
        isPlural = number != 1
    elif isinstance(number, (list, tuple, dict, set)):
        isPlural = len(number) != 1
    else:
        isPlural = number
    return plural if isPlural else singular
