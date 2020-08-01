
_notifyHandlers = {}
_chatStartHandler = None
_intents = set()
_botMessageHandlers = {}


class User:

    def __init__(self, channel, key):
        self._data = {}
        self._channel = channel
        self._key = key
        if _chatStartHandler is not None:
            _chatStartHandler(self)

    def notify(self, tag, data=None):
        for handler in _notifyHandlers.get(tag, []):
            handler(self, tag, data)

    def __getitem__(self, key):
        return self._data.get(key, None)

    def __setitem__(self, key, value):
        if value is None:
            self._data.pop(key)
        else:
            self._data[key] = value

    def __getstate__(self):
        return self._channel, self._key, self._data

    def __setstate__(self, state):
        self._channel, self._key, self._data = state

    def send(self, message):
        handler = _botMessageHandlers.get(self._channel, None)
        if handler is None:
            raise Exception(f'No bot message handler is defined for channel "{self._channel}"')
        handler(self._key, message)

    def __repr__(self):
        return f'{self.__class__.__qualname__}{self._channel, self._key}'

    def __str__(self):
        return str((self._channel, self._key))


def onNotify(tags):
    if not isinstance(tags, (list, set, tuple)):
        raise TypeError('Unexpected tags type')

    def wrapper(handler):
        for tag in tags:
            handlers = _notifyHandlers.get(tag, None)
            if handlers is None:
                _notifyHandlers[tag] = handlers = set()
            handlers.add(handler)
        return handler
    return wrapper


def onChatStart(handler):
    global _chatStartHandler
    if _chatStartHandler is not None:
        raise Exception('A chat start handler is already defined')
    _chatStartHandler = handler
    return handler


def intent(handler):
    _intents.add(handler)
    return handler


def onBotMessage(channel):
    def wrapper(handler):
        if channel in _botMessageHandlers:
            raise Exception(f'A bot message handler for channel "{channel}" is already defined')
        _botMessageHandlers[channel] = handler
    return wrapper


def _userMessage(user, message):
    bestValue = None
    best = []
    for intent in _intents:
        res = intent(user, message)
        value, action = res[0], res[1:]
        if len(best) == 0:
            bestValue = value
        if value > bestValue:
            bestValue = value
            best = [action]
        elif value == bestValue:
            best.append(action)
    if len(best) > 0:
        import random
        action = random.choice(best)
        action[0](user, *action[1:])