from .. import dispatcher

@dispatcher.onChatStart
def onChatStart(user):
    user.send('Hello!')

@dispatcher.intent
def didntUnderstand(user, message):
    return 0.5, _didntUnderstandAction

def _didntUnderstandAction(user):
    user.notify('didntUnderstand')
    user.send('Sorry, I did\'t understand.')
