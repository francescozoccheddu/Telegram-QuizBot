from enum import Enum, auto
from . import game


class YesNoAction(Enum):
    GIVE_UP = auto()
    ANSWER = auto()
    DO_RWA = auto()
    DO_SQ = auto()


class ChatGame(game.Game):

    def __init__(self):
        super().__init__()
        self._yesNoAction = None
        self._yesNoAnswerActionIndex = None

    @property
    def yesNoAction(self):
        return self._yesNoAction

    @property
    def yesNoAnswerActionIndex(self):
        return self._yesNoAnswerActionIndex

    @property
    def hasYesNoAction(self):
        return self._yesNoAction is not None

    def setYesNoAction(self, action, answerActionIndex=None):
        if not self._playing:
            raise Exception('Not playing')
        if not isinstance(action, YesNoAction):
            raise TypeError('Unexpected action')
        if action == YesNoAction.ANSWER and (not isinstance(answerActionIndex, int) or not (0 <= answerActionIndex < len(self._answers))):
            raise ValueError('Expected answer index')
        self._yesNoAction = action
        self._yesNoAnswerActionIndex = answerActionIndex

    def resetYesNoAction(self):
        self._yesNoAction = None
        self._yesNoAnswerActionIndex = None

    def __getstate__(self):
        return (self._yesNoAction, self._yesNoAnswerActionIndex, *super().__getstate__())

    def __setstate__(self, value):
        super().__setstate__(value[2:])
        self._yesNoAction, self._yesNoAnswerActionIndex = value[:2]
