
_channels = {}
_dataFile = 'users'


def store():
    from ..utils import resources
    resources.store(_dataFile, _channels)


def load():
    from ..utils import resources
    _users = resources.load(_dataFile)


def remove(channel, key, raiseIfMissing=False):
    users = _channels.get(channel, None)
    if users is not None:
        if key in users:
            del users[key]
            if len(users) == 0:
                del _channels[channel]
        elif raiseIfMissing:
            raise Exception(f'No user "{key}" in channel "{channel}" exists')
    elif raiseIfMissing:
        raise Exception(f'No channel "{channel}" exists')


def add(channel, key, raiseIfExists=False):
    from . import dispatcher
    users = _channels.get(channel, None)
    if users is None:
        _channels[channel] = users = {}
    if key not in users:
        users[key] = dispatcher.User(channel, key)
    elif raiseIfExists:
        raise Exception(f'User "{key}" already exists in channel "{channel}"')


def exists(channel, key):
    users = _channels.get(channel, None)
    return users is not None and key in users


def userMessage(channel, key, message, raiseIfMissing=True):
    from . import dispatcher
    users = _channels.get(channel, None)
    if users is not None:
        user = users.get(key, None)
        if user is None:
            if raiseIfMissing:
                raise Exception(f'User "{key}" already exists in channel "{channel}"')
            users[key] = user = dispatcher.User(channel, key)
        dispatcher._userMessage(user, message)
    elif raiseIfMissing:
        raise Exception(f'No channel "{channel}" exists')
