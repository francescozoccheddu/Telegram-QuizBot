from ..utils import string as s
from ..chatgame import YesNoAction
from .base import forceAnswer, forceGiveUp
from .lifelines import forceDoRwa, forceDoSq

_actionMapping = {
    YesNoAction.ANSWER: forceAnswer,
    YesNoAction.GIVE_UP: forceGiveUp,
    YesNoAction.DO_RWA: forceDoRwa,
    YesNoAction.DO_SQ: forceDoSq
}


def _confirm(user):
    g = user.data
    func = _actionMapping[g.yesNoAction]
    args = (g.yesNoAnswerActionIndex,) if g.yesNoAnswerActionIndex is not None else ()
    func(user, *args)


def yesNo(user, positive):
    g = user.data
    if g.hasYesNoAction:
        if positive:
            _confirm(user)
        else:
            user.send(s('cancelConfirm').f())
    else:
        from .base import didntUnderstandAction
        didntUnderstandAction(user)
    g.resetYesNoAction()


def reinforce(user, action, answerActionIndex=None):
    g = user.data
    if g.yesNoAction == action and g.yesNoAnswerActionIndex == answerActionIndex:
        _confirm(user)
        return True
    else:
        g.resetYesNoAction()
        return False
