from ...chat import chat
from .chatstart import chatStarted
from . import intents


_dispatcher = chat.Dispatcher()
_dispatcher.onUserCreated = chatStarted
_dispatcher.onUserMessage = intents.process


def dispatcher():
    return _dispatcher
