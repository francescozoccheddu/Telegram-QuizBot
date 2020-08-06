
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
        _printQuestion(user)


def formatQuestion(question, answers):
    msg = question
    for i, a in enumerate(answers):
        msg += f'\n{i + 1}) {a.rstrip(".")}' + (';' if i == len(answers) - 1 else '.')
    return msg


def _printQuestion(user):
    g = user.data
    user.send(formatQuestion(g.question, g.answers))
    from .lifelines import remind
    remind(user)


def _formatEndScore(recordScore, oldRecordScore):
    if oldRecordScore is not None:
        if oldRecordScore != recordScore:
            return 'Congratulations! This is your new record!'
        else:
            return f'You record is {recordScore}.'
    else:
        return ''


def _printStartMessage(user):
    user.send('Tell me when you want to start a new game.')


def _printEndScore(user):
    g = user.data
    user.send(_formatEndScore(g.recordScore, g.oldRecordScore))


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
                    user.send(f'Correct answer! Your score is {g.score}.')
                    _printQuestion(user)
                else:
                    user.send(f'Wrong answer! The correct one was {rightAnswer.rstrip(".")}.\n' +
                              f'Your score is {g.score}. {_formatEndScore(g.recordScore, g.oldRecordScore)}')
                    _printStartMessage(user)
            else:
                from ..chatgame import YesNoAction
                g.setYesNoAction(YesNoAction.ANSWER, answerIndex)
                user.send(f'{g.answers[answerIndex].rstrip(".")}.\nIs this your answer? Are you sure?')
    else:
        user.send('You are not playing!')


def _giveUp(user, force):
    g = user.data
    g.resetYesNoAction()
    if g.isPlaying:
        if force:
            g.giveUp()
            user.send(f'You gave up. Your score is {g.score}. {_formatEndScore(g.recordScore, g.oldRecordScore)}')
            _printStartMessage(user)
        else:
            from ..chatgame import YesNoAction
            g.setYesNoAction(YesNoAction.GIVE_UP)
            user.send('Are you sure you want to give up?')
    else:
        user.send('You are not playing!')


def answer(user, answerIndex):
    _answer(user, answerIndex, False)


def giveUp(user):
    _giveUp(user, False)


def forceAnswer(user, answerIndex):
    _answer(user, answerIndex, True)


def forceGiveUp(user):
    _giveUp(user, True)


def myRecord(user):
    # TODO
    pass


def myScore(user):
    # TODO
    pass


def myQuestion(user):
    # TODO
    pass
