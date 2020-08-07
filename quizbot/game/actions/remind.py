from ...utils import nlg


def score(user, allowWhenNotPlaying=False):
    g = user.data
    if g.isPlaying or allowWhenNotPlaying:
        user.send(f'Your score is {g.score}.')
    else:
        notPlaying(user)


def newRecordScore(user):
    g = user.data
    if g.oldRecordScore is not None and g.oldRecordScore > 0:
        if g.oldRecordScore != g.recordScore:
            user.send('Congratulations! This is your new record!')
        else:
            user.send(f'You record is {g.recordScore}.')


def recordScore(user):
    g = user.data
    if g.recordScore is not None and g.recordScore > 0:
        user.send(f'Your record score is {g.recordScore}.')
    else:
        user.send('You don\'t have a record score yet.')


def question(user):
    g = user.data
    msg = g.question
    for i, a in enumerate(g.answers):
        msg += f'\n{i + 1}) {a.rstrip(".")}' + (';' if i < len(g.answers) - 1 else '.')
    user.send(msg)


def lifelines(user):
    g = user.data
    if g.canDoRwa or g.canDoSq:
        msg = 'You can '
        if g.canDoRwa:
            from ..game import rwaAnswersCount
            k = rwaAnswersCount()
            msg += f'remove {nlg.card(k)} wrong answer{nlg.plur(k)}'
        if g.canDoSq:
            if g.canDoRwa:
                msg += ' or '
            msg += 'switch question'
        msg += ', if you want.'
        user.send(msg)
    else:
        user.send('You have no more aids, but if you are in trouble you can give up to double your score.')


def startMessage(user):
    user.send('Tell me when you want to start a new game.')


def notPlaying(user):
    user.send('You are not playing!')
