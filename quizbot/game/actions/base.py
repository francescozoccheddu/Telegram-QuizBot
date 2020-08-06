
def didntUnderstandAction(user):
    g = user.data
    g.resetYesNoAction()
    user.send('Sorry, I did\'t understand.')


def startNewGame(user):
    g = user.data
    g.resetYesNoAction()
    if g.isPlaying:
        from ..chatgame import YesNoAction
        g.setYesNoAction(YesNoAction.GIVE_UP)
        user.send('You have to finish the current match before starting a new one. Do you want to give up?')
    else:
        user.send('Let\'s start!')
        g.start()
        from . import remind
        remind.question(user)


def _answer(user, answerIndex, force):
    g = user.data
    g.resetYesNoAction()
    if g.isPlaying:
        if answerIndex in g.rwaIndices:
            user.send('I already told you that this is not the correct answer! Try with another one.')
        else:
            if force:
                rightAnswer = g.rightAnswer
                right = g.answer(answerIndex)
                if right:
                    from . import remind
                    user.send(f'Correct answer!')
                    remind.score(user)
                    remind.question(user)
                else:
                    from . import remind
                    user.send(f'Wrong answer! The correct one was {rightAnswer.rstrip(".")}.')
                    remind.score(user, True)
                    remind.newRecordScore(user)
                    remind.startMessage(user)
            else:
                from ..chatgame import YesNoAction
                g.setYesNoAction(YesNoAction.ANSWER, answerIndex)
                user.send(f'{g.answers[answerIndex].rstrip(".")}.\nIs this your answer? Are you sure?')
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
            user.send('You gave up.')
            remind.score(user, True)
            remind.newRecordScore(user)
            remind.startMessage(user)
        else:
            from ..chatgame import YesNoAction
            g.setYesNoAction(YesNoAction.GIVE_UP)
            user.send('Are you sure you want to give up?')
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
