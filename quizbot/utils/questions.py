
def years(right):
    import datetime
    from ..game.quiz import answersCount
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
