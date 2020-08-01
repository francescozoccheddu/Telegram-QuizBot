from ..chat import chat

_channel = 'clichat'
_key = None
_open = False
_defaultKey = "_clichat_default_key"


def defaultKey():
    return _defaultKey


@chat.onBotMessage(_channel)
def _onBotMessage(key, message):
    if _open and key == _key:
        print(f'B: {message}')


def start(key=_defaultKey, restart=True):
    global _key, _open
    _key = key
    _open = True
    if restart:
        chat.users.remove(_channel, key)
    print(f'C: CLIChat started.')
    if not chat.users.exists(_channel, _key):
        print(f'C: User added.')
        chat.users.add(_channel, key)
    try:
        while True:
            print('Y: ', end='')
            try:
                message = input()
            except KeyboardInterrupt:
                print()
                raise
            chat.users.userMessage(_channel, key, message)
    except KeyboardInterrupt:
        print(f'C: CLIChat closed by user.')
    _open = False


def channel():
    return _channel
