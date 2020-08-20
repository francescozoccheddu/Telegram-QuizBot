_defaultKey = "_clichat_default_key"
_cliTag = 'C'
_userTag = 'Y'
_botTag = 'B'


def defaultKey():
    return _defaultKey


def _print(tag, message, newLine=True):
    tag = f'{tag}: '
    content = tag
    for i, line in enumerate(message.splitlines()):
        if i > 0:
            content += '\n' + ' ' * len(tag)
        content += line
    print(content, end='\n' if newLine else '')


def _onBotMessage(ck, uk, message):
    _print(_botTag, message)


def start(channel, key=_defaultKey):

    # Set callback
    oldHandler = channel.onBotMessage
    channel.onBotMessage = _onBotMessage

    # Start
    _print(_cliTag, 'Chat started.')
    if not channel[key].isChatting:
        _print(_cliTag, 'User added.')
        channel[key].startChat()

    # Loop
    try:
        while True:
            _print(_userTag, '', False)
            try:
                message = input()
            except KeyboardInterrupt:
                print()
                raise
            channel[key].userMessage(message)
    except KeyboardInterrupt:
        _print(_cliTag, 'Chat closed by user.')

    # Restore callback
    channel.onBotMessage = oldHandler
