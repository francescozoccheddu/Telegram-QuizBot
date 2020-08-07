
def chatStarted(user):
    from ..chatgame import ChatGame
    from ..actions.remind import startMessage
    user.data = ChatGame()
    user.send('Hello!')
    startMessage(user)
