from ..dispatcher import onChatStart


@onChatStart
def greetings(user):
    user.send('Hello!')
