class UserDispatcherView:

    def __init__(self, data=None):
        self._messages = []
        self._data = data

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    def send(self, message):
        self._messages.append(message)

    @property
    def messages(self):
        return tuple(self._messages)


class UserView:

    def __init__(self, key, channel):
        self._key = key
        self._channel = channel

    @property
    def key(self):
        return self._key

    @property
    def channelKey(self):
        return self._channel.key

    @property
    def isChatting(self):
        channels = self._channel._exchange._channels
        return self._key in channels.get(self.channelKey, {})

    def startChat(self, raiseIfStarted=False):
        exchange = self._channel._exchange
        channels = exchange._channels
        users = channels.get(self.channelKey)
        if users is None:
            channels[self.channelKey] = users = {}
        if self._key not in users:
            view = UserDispatcherView()
            exchange.dispatcher.onUserCreated(view)
            users[self._key] = view.data
            for message in view.messages:
                self._channel.onBotMessage(self.channelKey, self._key, message)
            return True
        elif raiseIfStarted:
            raise Exception('Already started')
        else:
            return False

    def stopChat(self, raiseIfNotStarted=False):
        channels = self._channel._exchange._channels
        users = channels.get(self.channelKey)
        if users is not None and self._key in users:
            del users[self._key]
            if len(users) == 0:
                del channels[self.channelKey]
            return True
        elif raiseIfNotStarted:
            raise Exception('Not started')
        else:
            return False

    def userMessage(self, message, raiseIfNotStarted=False, startIfNotStarted=False):
        if not self.isChatting:
            if raiseIfNotStarted:
                raise Exception('Not started')
            if startIfNotStarted:
                self.startChat()
            else:
                return False
        exchange = self._channel._exchange
        users = exchange._channels[self.channelKey]
        view = UserDispatcherView(users[self._key])
        exchange.dispatcher.onUserMessage(view, message)
        users[self._key] = view.data
        for message in view.messages:
            self._channel.onBotMessage(self.channelKey, self._key, message)
        return True


class ChannelView:

    def __init__(self, key, exchange):
        self._key = key
        self._exchange = exchange

    @property
    def key(self):
        return self._key

    def __getitem__(self, key):
        return UserView(key, self)

    @property
    def chattingUsers(self):
        return [UserView(k, self) for k in self._exchange._channels.get(self._key, {})]

    @property
    def onBotMessage(self):
        return self._exchange._channelMessageHandlers.get(self._key, None)

    @onBotMessage.setter
    def onBotMessage(self, value):
        if value is not None:
            self._exchange._channelMessageHandlers[self._key] = value
        else:
            del self._exchange._channelMessageHandlers[self._key]


class Exchange:

    def __init__(self):
        self._channels = {}
        self._channelMessageHandlers = {}
        self._dispatcher = Dispatcher()

    def __getitem__(self, key):
        return ChannelView(key, self)

    @property
    def activeChannels(self):
        return [ChannelView(k, self) for k in (set(self._channels.keys()) | set(self._channelMessageHandlers.keys()))]

    @property
    def dispatcher(self):
        return self._dispatcher

    @dispatcher.setter
    def dispatcher(self, value):
        if not isinstance(value, Dispatcher):
            raise TypeError()
        self._dispatcher = value

    def __getstate__(self):
        return self._channels

    def __setstate__(self, state):
        self._channels = state
        self._channelMessageHandlers = {}
        self._dispatcher = Dispatcher()


class Dispatcher:

    def __init__(self):
        self._onUserMessage = None
        self._onUserCreated = None

    @property
    def onUserMessage(self):
        return self._onUserMessage

    @property
    def onUserCreated(self):
        return self._onUserCreated

    @onUserMessage.setter
    def onUserMessage(self, value):
        self._onUserMessage = value

    @onUserCreated.setter
    def onUserCreated(self, value):
        self._onUserCreated = value
