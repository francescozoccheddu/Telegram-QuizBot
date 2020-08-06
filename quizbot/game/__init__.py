from ..chat import onChatStart


def readyWithUI():
    from ..questions import quizzer
    quizzer.readyAllWithUI()


@onChatStart
def _chatStarted(user):
    from .chatgame import ChatGame
    from . import intents
    from ..questions import topics
    from .actions.remind import startMessage
    user.data = ChatGame()
    user.send('Hello!')
    startMessage(user)
