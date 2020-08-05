from ...dispatcher import intent
from .. import actions
from . import utils


@intent
def fallback(user, message):
    return 0.5, actions.didntUnderstandAction


@intent
def giveUp(user, message):
    syns = ['quit', 'stop', 'abandon', 'surrender', 'leave', 'give up']
    ignoredSyns = ['want', 'please', 'do', 'like', 'will', 'would']
    tlss = utils.tagAndLemmatizeSentences(message.lower(), [('give', 'up')])
    verbs = [w for s in tlss for (w, t) in s if t.startswith('VB')]
    singletons = utils.singleWordSentences(tlss, syns, utils.VERB)
    candidates = [w for w in verbs + singletons if utils.semanticSimilarity(w, ignoredSyns, utils.VERB, 0) < 0.5]
    confidence = utils.semanticSimilarity(candidates, syns, utils.VERB)
    return confidence, actions.giveUp


