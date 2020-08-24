from .resources import LazyJson

_numbers = LazyJson('other/nlgNumbers.json')


def _list(listOrStr):
    if isinstance(listOrStr, str):
        return [listOrStr]
    else:
        return listOrStr


def _first(listOrStr):
    if isinstance(listOrStr, str):
        return listOrStr
    else:
        return listOrStr[0]


def _flat(nestedList):
    return [ni for i in nestedList for ni in _list(i)]


def ord(number):
    if isinstance(number, int) and 1 <= number <= len(_numbers.ordinals):
        return _first(_numbers.ordinals[number - 1])
    else:
        return f'{number}{_numbers.ordinalSuffix}'


def card(number):
    if isinstance(number, int) and 0 <= number < len(_numbers.cardinals):
        return _first(_numbers.cardinals[number])
    else:
        return f'{number}'


def invCard(word):
    word = word.strip().lower()
    if word.isdigit():
        return int(word)
    for i, v in enumerate(_numbers.cardinals):
        if word in _list(v):
            return i
    return None


def invOrd(word):
    word = word.strip().lower()
    for suff in _list(_numbers.ordinalSuffix):
        if word.endswith(suff):
            number = word[:-len(suff)]
            if number.isdigit():
                return int(number)
    for i, v in enumerate(_numbers.ordinals):
        if word in _list(v):
            return i + 1
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


def ordMatcherPatterns():
    patterns = [
        {'label': 'ORDINAL', 'pattern': [{'LEMMA': {'IN': _flat(_numbers.ordinals)}}]}
    ]
    suffs = _list(_numbers.ordinalSuffix)
    if len(suffs) > 0:
        import re
        patterns += [
            {'label': 'ORDINAL', 'pattern': [{'LOWER': {'REGEX': f'[1-9][0-9]*({"|".join([re.escape(s) for s in suffs])})'}}]},
            {'label': 'ORDINAL', 'pattern': [{'IS_DIGIT': 'TRUE'}, {'LOWER': {'IN': suffs}}]}
        ]
    return patterns


def cardMatcherPatterns():
    patterns = [
        {'label': 'CARDINAL', 'pattern': [{'LEMMA': {'IN': _flat(_numbers.cardinals)}}]}
    ]
    suffs = _list(_numbers.ordinalSuffix)
    if len(suffs) > 0:
        patterns += [
            {'label': 'CARDINAL', 'pattern': [{'IS_DIGIT': 'TRUE'}, {'LOWER': {'IN': suffs}, 'OP': '!'}]}
        ]
    else:
        patterns += [
            {'label': 'CARDINAL', 'pattern': [{'IS_DIGIT': 'TRUE'}]}
        ]
    return patterns
