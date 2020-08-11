from .resources import LazyJson

_numbers = LazyJson('other/nlgNumbers.json')


def ord(number):
    if isinstance(number, int) and 1 <= number <= len(_numbers.ordinals):
        return _numbers.ordinals[number - 1]
    else:
        return f'{number}{_numbers.ordinalSuffix}'


def card(number):
    if isinstance(number, int) and 0 <= number < len(_numbers.cardinals):
        return _numbers.cardinals[number]
    else:
        return f'{number}'

def invCard(word):
    word = word.strip().lower()
    if word.isdigit():
        return int(word)
    try:
        return _numbers.cardinals.index(word)
    except ValueError:
        return None

def invOrd(word):
    word = word.strip().lower()
    if word.endswith(_numbers.ordinalSuffix):
        number = word[:-len(_numbers.ordinalSuffix)]
        if number.isdigit():
            return int(number)
    try:
        return _numbers.ordinals.index(word) + 1
    except ValueError:
        return None


def invNum(word):
    card = invCard(word)
    if card is None:
        return invOrd(word)
    else:
        return card


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
