from .. import chat

_channel = 'clichat'
_defaultKey = "_clichat_default_key"


def defaultKey():
    return _defaultKey


@chat.onBotMessage(_channel)
def _onBotMessage(key, message):
    print(f'B: {message}')


def start(key=_defaultKey):
    from .. import game
    game.readyWithUI()
    print(f'C: CLIChat started.')
    if not chat.users.exists(_channel, key):
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


def channel():
    return _channel
