from ..chatgame import YesNoAction
from .base import forceAnswer, forceGiveUp
from .lifelines import forceDoRwa, forceDoSq

_actionMapping = {
    YesNoAction.ANSWER: forceAnswer,
    YesNoAction.GIVE_UP: forceGiveUp,
    YesNoAction.DO_RWA: forceDoRwa,
    YesNoAction.DO_SQ: forceDoSq
}


def yesNo(user, positive):
    g = user.data
    if g.hasYesNoAction:
        if positive:
            func = _actionMapping[g.yesNoAction]
            args = (g.yesNoAnswerActionIndex,) if g.yesNoAnswerActionIndex is not None else ()
            func(user, *args)
        else:
            user.send('Ok, think about it.')
    else:
        from .base import didntUnderstandAction
        didntUnderstandAction(user)
    g.resetYesNoAction()
