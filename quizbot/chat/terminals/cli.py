_defaultKey = "_clichat_default_key"


def defaultKey():
    return _defaultKey


def _onBotMessage(ck, uk, message):
    print(f'B: {message}')


def start(channel, key=_defaultKey):

    # Set callback
    oldHandler = channel.onBotMessage
    channel.onBotMessage = _onBotMessage

    # Start
    print(f'C: CLIChat started.')
    if not channel[key].isChatting:
        print(f'C: User added.')
        channel[key].startChat()
    
    # Loop
    try:
        while True:
            print('Y: ', end='')
            try:
                message = input()
            except KeyboardInterrupt:
                print()
                raise
            channel[key].userMessage(message)
    except KeyboardInterrupt:
        print(f'C: CLIChat closed by user.')

    # Restore callback
    channel.onBotMessage = oldHandler
