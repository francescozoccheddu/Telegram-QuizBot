
_config = None


def _loadConfig():
    global _config
    if _config is None:
        from ...utils import resources
        _config = resources.json('telegram.json')


def start(channel):
    _loadConfig()

    # Set callbacks
    oldHandler = channel.onBotMessage
    from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
    updater = Updater(token=_config['token'], use_context=True)

    def onBotMessage(ck, uk, message):
        updater.bot.send_message(uk, message)

    def onUserStartCommand(update, context):
        id = update.effective_chat.id
        channel[id].stopChat()
        channel[id].startChat()

    def onUserMessage(update, context):
        id = update.effective_chat.id
        channel[id].userMessage(update.message.text)

    channel.onBotMessage = onBotMessage
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', onUserStartCommand))
    dispatcher.add_handler(MessageHandler(Filters.text, onUserMessage))

    # Loop
    print('Running...')
    updater.start_polling()
    updater.idle()
    
    # Restore callbacks
    channel.onBotMessage = oldHandler
