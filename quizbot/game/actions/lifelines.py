from ..utils import string as s
from ...utils import nlg
from ..chatgame import YesNoAction
from . import remind


def _doRwa(user, force):
    g = user.data
    if force:
        g.resetYesNoAction()
    else:
        from . import confirm
        if confirm.reinforce(user, YesNoAction.DO_RWA):
            return
    if g.isPlaying:
        from ..game import config
        k = config().rwaAnswersCount
        if g.canDoRwa:
            if force:
                g.doRwa()
                wrongOrdinal = [nlg.ord(i + 1) for i in sorted(g.rwaIndices)]
                ordinals = nlg.join(wrongOrdinal, s('rwaHelpConjunction').s)
                user.send(s('rwaHelpInvoked').p(len(wrongOrdinal), answers=ordinals))
            else:
                g.setYesNoAction(YesNoAction.DO_RWA)
                turns = config().rwaCooldownTurns
                user.send(s('askForRwaConfirm').p(k, answers=nlg.card(k)))
                user.send(s('lifelineCooldownWarning').p(turns, turns=nlg.card(turns)))
        else:
            turns = g.rwaCooldown
            user.send(s('rwaCooldownWait').p(turns, turns=nlg.card(turns)))

    else:
        remind.notPlaying(user)


def _doSq(user, force):
    g = user.data
    if force:
        g.resetYesNoAction()
    else:
        from . import confirm
        if confirm.reinforce(user, YesNoAction.DO_SQ):
            return
    if g.isPlaying:
        if g.canDoSq:
            if force:
                g.doSq()
                user.send(s('sqHelpInvoked').s)
                remind.question(user)
            else:
                from ..game import config
                g.setYesNoAction(YesNoAction.DO_SQ)
                turns = config().sqCooldownTurns
                user.send(s('askForSqConfirm').s)
                user.send(s('lifelineCooldownWarning').p(turns, turns=nlg.card(turns)))
        else:
            turns = g.sqCooldown
            user.send(s('sqCooldownWait').p(turns, turns=nlg.card(turns)))
    else:
        remind.notPlaying(user)


def doRwa(user):
    _doRwa(user, False)


def doSq(user):
    _doSq(user, False)


def forceDoRwa(user):
    _doRwa(user, True)


def forceDoSq(user):
    _doSq(user, True)
