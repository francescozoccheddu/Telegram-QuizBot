from ...chat import chat
from .chatstart import chatStarted


def _userMessage(user, message):
    from . import intents
    ints = [intents.answerByIndex, intents.fallback, intents.giveUp, intents.hint,
            intents.removeTwoWrongQuestions, intents.startGame, intents.switchQuestion,
            intents.yes, intents.no]
    conf, act, args = 0, None, []
    for i in ints:
        res = i(user, message)
        if res[0] > conf:
            conf = res[0]
            act = res[1]
            args = res[2:]
    act(user, *args)


_dispatcher = chat.Dispatcher()
_dispatcher.onUserCreated = chatStarted
_dispatcher.onUserMessage = _userMessage


def dispatcher():
    return _dispatcher
