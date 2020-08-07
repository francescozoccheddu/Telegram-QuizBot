from ...utils import nlg


def remind(user):
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


def _doRwa(user, force):
    g = user.data
    g.resetYesNoAction()
    if g.isPlaying:
        from ..game import rwaAnswersCount
        k = rwaAnswersCount()
        if g.canDoRwa:
            if force:
                g.doRwa()
                wrongCardinal = [nlg.card(i + 1) for i in g.rwaIndices]
                user.send(f'Answer{nlg.plur(k)} number {nlg.join(wrongCardinal)} {nlg.plur(k, "are", "is")} wrong.')
            else:
                from ..chatgame import YesNoAction
                from ..game import rwaCooldownTurns
                g.setYesNoAction(YesNoAction.DO_RWA)
                turns = rwaCooldownTurns()
                user.send(f'Are you sure you want to remove {nlg.card(k)} wrong answer{nlg.plur(k)}?\n' +
                          f'You won\'t be able to use this lifeline again for {turns} turn{nlg.plur(turns)}.')
        else:
            turns = g.rwaCooldown
            user.send(f'You have to wait {turns} more turn{nlg.plur(turns)} to remove {nlg.card(k)} wrong answer{nlg.plur(k)}.')
    else:
        from . import remind
        remind.notPlaying(user)


def _doSq(user, force):
    g = user.data
    g.resetYesNoAction()
    if g.isPlaying:
        if g.canDoSq:
            if force:
                from . import remind
                g.doSq()
                user.send('Here is another question...')
                remind.question(user)
            else:
                from ..chatgame import YesNoAction
                from ..game import sqCooldownTurns
                g.setYesNoAction(YesNoAction.DO_SQ)
                turns = sqCooldownTurns()
                user.send(f'Are you sure you want to switch the question?\n' +
                          f'You won\'t be able to use this lifeline again for {turns} turn{nlg.plur(turns)}.')
        else:
            turns = g.sqCooldown
            user.send(f'You have to wait {turns} more turn{nlg.plur(turns)} to switch the question again.')
    else:
        from . import remind
        remind.notPlaying(user)


def doRwa(user):
    _doRwa(user, False)


def doSq(user):
    _doSq(user, False)


def forceDoRwa(user):
    _doRwa(user, True)


def forceDoSq(user):
    _doSq(user, True)
