from ...dispatcher import intent
from .. import actions
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

_stopWords = set(stopwords.words('english'))

@intent
def didntUnderstand(user, message):
    return 0.5, actions.didntUnderstandAction


@intent
def gaveUp(user, message):
    sentences = sent_tokenize(message)
    confidence = 0
    for sentence in sentences:
        words = word_tokenize(sentence)
        words = [w in words if w not in _stopWords]
        
    if len(sentences) > 0:
        confidence /= len(sentences)
    return confidence, actions.giveUp
