from ..utils import string as s
from . import remind
from ..chatgame import YesNoAction


def didntUnderstandAction(user):
    g = user.data
    g.resetYesNoAction()
    user.send(s('didntUnderstand').f())


def startNewGame(user):
    g = user.data
    g.resetYesNoAction()
    if g.isPlaying:
        g.setYesNoAction(YesNoAction.GIVE_UP)
        user.send(s('cannotStartWhilePlaying').f())
    else:
        user.send(s('letsStart').f())
        g.start()
        remind.question(user)


def _answer(user, answerIndex, force):
    g = user.data
    if force:
        g.resetYesNoAction()
    else:
        from . import confirm
        if confirm.reinforce(user, YesNoAction.ANSWER, answerIndex):
            return
    if g.isPlaying:
        if answerIndex in g.rwaIndices:
            user.send(s('rwaKnownWrongAnswer').f())
        else:
            if force:
                rightAnswer = g.rightAnswer
                right = g.answer(answerIndex)
                if right:
                    user.send(s('correctAnswer').f())
                    remind.score(user)
                    remind.question(user)
                else:
                    user.send(s('wrongAnswer').f(answer=rightAnswer))
                    remind.score(user, True)
                    remind.newRecordScore(user)
                    remind.startMessage(user)
            else:
                g.setYesNoAction(YesNoAction.ANSWER, answerIndex)
                user.send(s('askForAnswerConfirm').f(answer=g.answers[answerIndex]))
    else:
        remind.notPlaying(user)


def _giveUp(user, force):
    g = user.data
    if force:
        g.resetYesNoAction()
    else:
        from . import confirm
        if confirm.reinforce(user, YesNoAction.GIVE_UP):
            return
    if g.isPlaying:
        if force:
            g.giveUp()
            user.send(s('gaveUp').f())
            remind.score(user, True)
            remind.newRecordScore(user)
            remind.startMessage(user)
        else:
            g.setYesNoAction(YesNoAction.GIVE_UP)
            user.send(s('askForGiveUpConfirm').f())
    else:
        remind.notPlaying(user)


def answer(user, answerIndex):
    _answer(user, answerIndex, False)


def giveUp(user):
    _giveUp(user, False)


def forceAnswer(user, answerIndex):
    _answer(user, answerIndex, True)


def forceGiveUp(user):
    _giveUp(user, True)
