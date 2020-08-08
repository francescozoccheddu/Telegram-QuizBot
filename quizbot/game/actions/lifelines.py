from .utils import string as s
from ...utils import nlg


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
                cardinals = nlg.join(wrongCardinal, s('rwaHelpConjunction').f())
                user.send(s('rwaHelpInvoked').p(len(wrongCardinal), answers=cardinals))
            else:
                from ..chatgame import YesNoAction
                from ..game import rwaCooldownTurns
                g.setYesNoAction(YesNoAction.DO_RWA)
                turns = rwaCooldownTurns()
                user.send(s('askForRwaConfirm').p(k, answers=k))
                user.send(s('lifelineCooldownWarning').p(turns, turns=turns))
        else:
            turns = g.rwaCooldown
            user.send(s('lifelineCooldownWait').p(turns, turns=turns))

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
                user.send(s('sqHelpInvoked').f())
                remind.question(user)
            else:
                from ..chatgame import YesNoAction
                from ..game import sqCooldownTurns
                g.setYesNoAction(YesNoAction.DO_SQ)
                turns = sqCooldownTurns()
                user.send(s('askForSqConfirm').f())
                user.send(s('lifelineCooldownWarning').p(turns, turns=turns))
        else:
            turns = g.sqCooldown
            user.send(s('lifelineCooldownWait').p(turns, turns=turns))
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
