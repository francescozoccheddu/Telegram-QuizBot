from ..utils import string as s
from ...utils import nlg


def score(user, allowWhenNotPlaying=False):
    g = user.data
    if g.isPlaying or allowWhenNotPlaying:
        user.send(s('score').f(score=g.score))
    else:
        notPlaying(user)


def newRecordScore(user):
    g = user.data
    if g.oldRecordScore is not None and g.oldRecordScore > 0:
        if g.oldRecordScore != g.recordScore:
            user.send(s('newRecord').s)
        else:
            user.send(s('recordScore').f(score=g.recordScore))


def recordScore(user):
    g = user.data
    if g.recordScore is not None and g.recordScore > 0:
        user.send(s('recordScore').f(score=g.recordScore))
    else:
        user.send(s('noRecord').s)


def question(user):
    g = user.data
    if g.isPlaying:
        msg = g.question
        for i, a in enumerate(g.answers):
            msg += f'\n{i + 1}) {a.rstrip(".")}' + (';' if i < len(g.answers) - 1 else '.')
        user.send(msg)
    else:
        notPlaying(user)


def lifelines(user, alsoGiveUp=False):
    g = user.data
    if g.isPlaying:
        if g.canDoRwa or g.canDoSq:
            parts = []
            if g.canDoRwa:
                from ..game import config
                k = config().rwaAnswersCount
                parts.append(s('rwaDescriptionPart').p(k, answers=nlg.card(k)))
            if g.canDoSq:
                parts.append(s('sqDescriptionPart').s)
            lifelines = nlg.join(parts, s('lifelinesDescriptionConjunction').s)
            user.send(s('lifelinesDescription').f(lifelines=lifelines))
            if alsoGiveUp:
                user.send(s('lifelinesGiveUpDescription').s)
        else:
            user.send(s('noLifelinesDescription').s)
    else:
        notPlaying(user)


def startMessage(user):
    help(user)


def notPlaying(user):
    user.send(s('notPlaying').s)


def help(user):
    g = user.data
    if g.isPlaying:
        lifelines(user, True)
    else:
        user.send(s('tellMeWhenToStart').s)
