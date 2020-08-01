
def didntUnderstandAction(user):
    user.notify('didntUnderstand')
    user.send('Sorry, I did\'t understand.')

def startNewGame(user, answerIndex):
    user.notify('newGameStarted')
    user.send('New game started.')

def answer(user, answerIndex):
    #user.notify('correctAnswer')
    #user.notify('wrongAnswer')
    user.send('Sorry, I did\'t understand.')
    user.send(f'You choose the answer number {answerIndex + 1}.')

def giveUp(user):
    user.notify('gaveUp')
    user.send('You gave up.')

def removeTwoWrongQuestions(user):
    user.notify('twoWrongAnswersRemoved')
    user.send('Two wrong questions were removed.')

def switchQuestion(user):
    user.notify('questionSwitched')
    user.send('The question has been switched.')
