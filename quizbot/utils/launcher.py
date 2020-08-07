_usersFile = None


def _loadConfig():
    global _usersFile
    if _usersFile is None:
        from . import resources
        _usersFile = resources.json('users.json')['dataFile']


def setupChannelMap(load=True, output=True, outputFailures=True):
    _loadConfig()
    if output:
        print('Loading game...')
    from ..game.dispatcher.dispatcher import dispatcher
    from ..questions import questions
    from ..game import game
    from ..utils import data
    questions.load(output, outputFailures)
    game.setQuiz(questions.quiz())
    channels = data.loadOr(_usersFile) if load else None
    if channels is None:
        from ..chat import chat
        channels = chat.ChannelMap()
    channels.dispatcher = dispatcher()
    return channels


def saveChannelMap(channelMap):
    _loadConfig()
    from ..utils import data
    data.store(_usersFile, channelMap)


def fromcli(args):

    # Parse args
    import argparse
    parser = argparse.ArgumentParser(description='QuizBot Telegram bot.')
    parser.add_argument('--cli', metavar='USER', type=str,
                        action='store', nargs='?', const=True, default=None,
                        help='Starts a CLI to chat with the bot as <USER> (or as the default user if unspecified) instead of launching the Telegram bot')
    actionGroup = parser.add_mutually_exclusive_group()
    actionGroup.add_argument('--clear_usr', type=str,
                             action='store', metavar='USER', nargs='?', const=True, default=None,
                             help='Clear <USER>\'s data (or clear all users\' data if unspecified)')
    actionGroup.add_argument('--list_usr', metavar='USER', type=str,
                             action='store', nargs='?', const=True, default=None,
                             help='Check whether <USER> exists or list all the users if unspecified')
    dataGroup = parser.add_mutually_exclusive_group()
    dataGroup.add_argument('--dont_load', action='store_true', help='Don\'t load or store any user data')
    dataGroup.add_argument('--dont_store', action='store_true', help='Don\' store any user data on exit')
    pargs = parser.parse_args()
    if isinstance(pargs.cli, str) and (pargs.clear_usr is not None or pargs.list_usr is not None):
        parser.error('Cannot specify <USER> in --cli argument when --clear_usr or --list_usr are specified')
    if (pargs.dont_load or pargs.dont_store) and (pargs.clear_usr is not None or pargs.list_usr is not None):
        parser.error('Cannot specify --dont_load or --dont_store arguments when --clear_usr or --list_usr are specified')

    channels = setupChannelMap(not pargs.dont_load)

    # Do chat
    try:
        if pargs.cli:
            from ..chat.terminals import cli
            terminal = cli
            channel = channels['cli']
        else:
            from ..chat.terminals import telegram
            terminal = telegram
            channel = channels['telegram']
        if pargs.clear_usr is not None:
            if isinstance(pargs.clear_usr, str):
                stopped = channel[pargs.clear_usr].stopChat()
                print(int(stopped))
            else:
                users = channel.chattingUsers
                for u in users:
                    u.stopChat()
                print(len(users))
        elif pargs.list_usr is not None:
            if isinstance(pargs.list_usr, str):
                chatting = channel[pargs.list_usr].isChatting
                print(int(chatting))
            else:
                for u in channel.chattingUsers:
                    print(u.key)
        else:
            args = [pargs.cli] if isinstance(pargs.cli, str) else []
            terminal.start(channel, *args)
    finally:
        pass

    saveChannelMap(channels)


def main():
    import sys
    fromcli(sys.argv)


if __name__ == "__main__":
    main()
