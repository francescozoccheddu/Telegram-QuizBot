from .utils import string as s

def didntUnderstandAction(user):
    g = user.data
    g.resetYesNoAction()
    user.send(s('didntUnderstand').f())


def startNewGame(user):
    g = user.data
    g.resetYesNoAction()
    if g.isPlaying:
        from ..chatgame import YesNoAction
        g.setYesNoAction(YesNoAction.GIVE_UP)
        user.send(s('cannotStartWhilePlaying').f())
    else:
        user.send(s('letsStart').f())
        g.start()
        from . import remind
        remind.question(user)


def _answer(user, answerIndex, force):
    g = user.data
    g.resetYesNoAction()
    if g.isPlaying:
        if answerIndex in g.rwaIndices:
            user.send(s('rwaKnownWrongAnswer').f())
        else:
            if force:
                rightAnswer = g.rightAnswer
                right = g.answer(answerIndex)
                if right:
                    from . import remind
                    user.send(s('correctAnswer').f())
                    remind.score(user)
                    remind.question(user)
                else:
                    from . import remind
                    user.send(s('wrongAnswer').f(answer=rightAnswer))
                    remind.score(user, True)
                    remind.newRecordScore(user)
                    remind.startMessage(user)
            else:
                from ..chatgame import YesNoAction
                g.setYesNoAction(YesNoAction.ANSWER, answerIndex)
                user.send(s('askForAnswerConfirm').f(answer=g.answers[answerIndex]))
    else:
        from . import remind
        remind.notPlaying(user)


def _giveUp(user, force):
    g = user.data
    g.resetYesNoAction()
    if g.isPlaying:
        if force:
            g.giveUp()
            from . import remind
            user.send(s('gaveUp').f())
            remind.score(user, True)
            remind.newRecordScore(user)
            remind.startMessage(user)
        else:
            from ..chatgame import YesNoAction
            g.setYesNoAction(YesNoAction.GIVE_UP)
            user.send(s('askForGiveUpConfirm').f())
    else:
        from . import remind
        remind.notPlaying(user)


def answer(user, answerIndex):
    _answer(user, answerIndex, False)


def giveUp(user):
    _giveUp(user, False)


def forceAnswer(user, answerIndex):
    _answer(user, answerIndex, True)


def forceGiveUp(user):
    _giveUp(user, True)
