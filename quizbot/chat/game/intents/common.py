from ...dispatcher import intent
from .. import actions


@intent
def didntUnderstand(user, message):
    return 0.5, actions.didntUnderstandAction


@intent
def gaveUp(user, message):
    return 0, None
