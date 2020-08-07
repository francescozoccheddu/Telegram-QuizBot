
def ord(number):
    if isinstance(number, int) and 1 <= number <= 9:
        return {
            1: 'first',
            2: 'second',
            3: 'third',
            4: 'fourth',
            5: 'fifth',
            6: 'sixth',
            7: 'seventh',
            8: 'eight',
            9: 'ninth'
        }[number]
    else:
        return f'{number}st'


def card(number):
    if isinstance(number, int) and 1 <= number <= 9:
        return {
            1: 'one',
            2: 'two',
            3: 'three',
            4: 'four',
            5: 'five',
            6: 'six',
            7: 'seven',
            8: 'eight',
            9: 'nine'
        }[number]
    else:
        return str(number)


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
