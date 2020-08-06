from . import utils as ut


def remind(user):
    g = user.data
    if g.canDoRwa or g.canDoSq:
        msg = 'Remember that you can '
        if g.canDoRwa:
            from ..game import rwaAnswersCount
            k = rwaAnswersCount()
            msg += f'remove {ut.cardinal(k)} wrong answer{ut.plural(k)}'
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
                wrongCardinal = [ut.cardinal(i + 1) for i in g.rwaIndices]
                user.send(f'Answer{ut.plural(k)} number {ut.join(wrongCardinal)} {ut.plural(k, "are", "is")} wrong.')
            else:
                from ..chatgame import YesNoAction
                from ..game import rwaCooldownTurns
                g.setYesNoAction(YesNoAction.DO_RWA)
                turns = rwaCooldownTurns()
                user.send(f'Are you sure you want to remove {ut.cardinal(k)} wrong answer{ut.plural(k)}?\n' + 
                    f'You won\'t be able to use this lifeline again for {turns} turn{ut.plural(turns)}.')
        else:
            turns = g.rwaCooldown
            user.send(f'You have to wait {turns} more turn{ut.plural(turns)} to remove {ut.cardinal(k)} wrong answer{ut.plural(k)}.')
    else:
        user.send('We are not playing yet!')


def _doSq(user, force):
    g = user.data
    g.resetYesNoAction()
    if g.isPlaying:
        if g.canDoSq:
            if force:
                from . import base
                g.doSq()
                msg = 'Here is another question:\n'
                msg += base.formatQuestion(g.question, g.answers)
                user.send(msg)
            else:
                from ..chatgame import YesNoAction
                from ..game import sqCooldownTurns
                g.setYesNoAction(YesNoAction.DO_SQ)
                turns = sqCooldownTurns()
                user.send(f'Are you sure you want to switch the question?\n' + 
                    f'You won\'t be able to use this lifeline again for {turns} turn{ut.plural(turns)}.')
        else:
            turns = g.sqCooldown
            user.send(f'You have to wait {turns} more turn{ut.plural(turns)} to switch the question again.')
    else:
        user.send('We are not playing yet!')


def doRwa(user):
    _doRwa(user, False)


def doSq(user):
    _doSq(user, False)


def forceDoRwa(user):
    _doRwa(user, True)


def forceDoSq(user):
    _doSq(user, True)
