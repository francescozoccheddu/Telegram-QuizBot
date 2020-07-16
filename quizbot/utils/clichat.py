
from ..game import dispatcher, users

_channel = 'clichat'
_key = None
_open = False
_defaultKey = None


def defaultKey():
    return _defaultKey


@dispatcher.onBotMessage(_channel)
def _onBotMessage(key, message):
    if _open and key == _key:
        print(f'B: {message}')


def start(key=_defaultKey, restart=True):
    print(f'C: CLIChat started.')
    global _key, _open
    _key = key
    _open = True
    if restart:
        remove(key)
    if not users.exists(_channel, _key):
        print(f'C: User added.')
        users.add(_channel, key)
    try:
        while True:
            print('Y: ', end='')
            try:
                message = input()
            except KeyboardInterrupt:
                print()
                raise
            users.userMessage(_channel, key, message)
    except KeyboardInterrupt:
        print(f'C: CLIChat closed by user.')
        pass
    _open = False


def remove(key=_defaultKey):
    users.remove(_channel, key)
