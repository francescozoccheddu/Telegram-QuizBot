def lin(x):
    return x


def inv(x):
    return 1 - x


def slowIn(x):
    return x * x


def slowOut(x):
    return x * (2 - x)


def slowInOut(x):
    return 2 * x * x if x < 0.5 else (4 - 2 * x) * x - 1
