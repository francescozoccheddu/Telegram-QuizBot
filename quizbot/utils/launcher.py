
def fromcli(args):
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

    from .. import chat
    if not pargs.dont_load and not pargs.dont_store:
        chat.users.load()
    try:
        if pargs.cli:
            from ..interfaces import cli
            interface = cli
        else:
            from ..interfaces import telegram
            interface = telegram
        if pargs.clear_usr is not None:
            if isinstance(pargs.clear_usr, str):
                print(int(chat.users.remove(interface.channel(), pargs.clear_usr)))
            else:
                print(chat.users.clearChannel(interface.channel()))
        elif pargs.list_usr is not None:
            if isinstance(pargs.list_usr, str):
                print(int(chat.users.exists(interface.channel(), pargs.list_usr)))
            else:
                for k in chat.users.channelKeys(interface.channel()):
                    print(k)
        else:
            args = [pargs.cli] if isinstance(pargs.cli, str) else []
            interface.start(*args)
    finally:
        pass
    if not pargs.dont_load and not pargs.dont_store and pargs.list_usr is None:
        chat.users.store()


def main():
    import sys
    fromcli(sys.argv)


if __name__ == "__main__":
    main()
