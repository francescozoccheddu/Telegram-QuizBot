from ..utils import string as s

def chatStarted(user):
    from ..chatgame import ChatGame
    from ..actions.remind import startMessage
    user.data = ChatGame()
    user.send(s('chatStarted').s)
    startMessage(user)
