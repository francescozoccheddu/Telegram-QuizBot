from .resources import Config

_config = Config('configs/launcher.json')


def loadExchange():
    from . import data
    exchange = data.loadOr(_config.exchangeFile)
    if exchange is None:
        from ..chat import chat
        exchange = chat.Exchange()
    return exchange


def loadDispatcher(output=True, outputFailures=True):
    from ..game.dispatcher.dispatcher import dispatcher
    from ..questions import questions
    questions.load(output, outputFailures)
    return dispatcher()


def loadExchangeAndDispatcher(loadEx=True, loadDisp=True, output=True, outputFailures=True):
    if output:
        print('Loading game...')
    from ..chat.chat import Exchange
    exchange = loadExchange() if loadEx else Exchange()
    if loadDisp:
        from ..game import game
        from ..questions import questions
        exchange.dispatcher = loadDispatcher(output, outputFailures)
        game.setQuiz(questions.quiz())
    return exchange


def saveExchange(exchange):
    from ..utils import data
    data.store(_config.exchangeFile, exchange)


def fromCli(args):

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
    dataGroup.add_argument('--dont_save', action='store_true', help='Don\' store any user data on exit')
    pargs = parser.parse_args()
    adminAction = pargs.clear_usr is not None or pargs.list_usr is not None
    if isinstance(pargs.cli, str) and adminAction:
        parser.error('Cannot specify <USER> in --cli argument when --clear_usr or --list_usr are specified')
    if (pargs.dont_load or pargs.dont_save) and adminAction:
        parser.error('Cannot specify --dont_load or --dont_save arguments when --clear_usr or --list_usr are specified')

    exchange = loadExchangeAndDispatcher(not pargs.dont_load, not adminAction, not adminAction, not adminAction)

    try:
        if pargs.cli:
            from ..chat.terminals import cli
            terminal = cli
            channel = exchange[_config.cliChannel]
        else:
            from ..chat.terminals import telegram
            terminal = telegram
            channel = exchange[_config.telegramChannel]
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

    if not pargs.dont_load and not pargs.dont_save and pargs.list_usr is None:
        saveExchange(exchange)


def main():
    import sys
    fromCli(sys.argv)


if __name__ == "__main__":
    main()
