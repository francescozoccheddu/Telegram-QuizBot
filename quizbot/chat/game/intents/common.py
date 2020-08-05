from ...dispatcher import intent
from .. import actions
from . import utils


@intent
def fallback(user, message):
    return 0.5, actions.didntUnderstandAction


@intent
def giveUp(user, message):
    verbSyns = ['quit', 'stop', 'abandon', 'surrender', 'leave', 'give up']
    tlss = utils.tagAndLemmatizeSentences(message.lower(), [('give', 'up')])
    verbs = utils.withPOS(tlss, 'VB')
    singletons = utils.singleWordSentences(tlss)
    candidates = utils.withoutUselessVerbs(verbs + singletons)
    confidence = utils.semanticSimilarity(candidates, verbSyns, utils.VERB, 0)
    return confidence, actions.giveUp


@intent
def switchQuestion(user, message):
    verbSyns = ['change', 'switch', 'replace', 'swap']
    nounSyns = ['question', 'quiz']
    adjectiveSyns = ['new', 'different']
    determinantSyns = ['another']
    tlss = utils.tagAndLemmatizeSentences(message.lower())
    verbs = utils.withoutUselessVerbs(utils.withPOS(tlss, 'VB'))
    nouns = utils.withPOS(tlss, 'NN')
    adjectives = utils.withPOS(tlss, 'JJ')
    determinants = utils.withPOS(tlss, 'DT')
    verbSim = utils.semanticSimilarity(verbs, verbSyns, utils.VERB, 0.2)
    nounSim = utils.semanticSimilarity(nouns, nounSyns, utils.NOUN, 0.2)
    adjectiveSim = utils.semanticSimilarity(adjectives, adjectiveSyns, utils.ADJ, 0.2)
    determinantSim = utils.semanticSimilarity(determinants, determinantSyns, None, 0.2)
    confidence = utils.optimisticMean([verbSim, nounSim, max(adjectiveSim, determinantSim)], weights=[3, 1, 2])
    return confidence, actions.switchQuestion


@intent
def removeTwoWrongQuestions(user, message):
    verbSyns = ['remove', 'delete', 'hide']
    nounSyns = ['answer', 'response']
    adjectiveSyns = ['wrong', 'incorrect']
    numberSyns = ['two']
    tlss = utils.tagAndLemmatizeSentences(message.lower())
    verbs = utils.withoutUselessVerbs(utils.withPOS(tlss, 'VB'))
    nouns = utils.withPOS(tlss, 'NN')
    adjectives = utils.withPOS(tlss, 'JJ')
    numbers = utils.withPOS(tlss, 'CD')
    verbSim = utils.semanticSimilarity(verbs, verbSyns, utils.VERB, 0.2)
    nounSim = utils.semanticSimilarity(nouns, nounSyns, utils.NOUN, 0.2)
    adjectiveSim = utils.semanticSimilarity(adjectives, adjectiveSyns, utils.ADJ, 0.2)
    numberSim = utils.semanticSimilarity(numbers, numberSyns, None, 0.2)
    confidence = utils.optimisticMean([verbSim, nounSim, adjectiveSim, numberSim], weights=[3, 1, 2, 0.5])
    return confidence, actions.removeTwoWrongQuestions


@intent
def hint(user, message):
    nounSyns = ['help', 'hint', 'aid']
    tlss = utils.tagAndLemmatizeSentences(message.lower())
    nouns = utils.withPOS(tlss, 'NN')
    confidence = utils.semanticSimilarity(nouns, nounSyns, utils.NOUN, 0)
    return confidence, actions.removeTwoWrongQuestions


@intent
def startGame(user, message):
    verbSyns = ['start', 'begin', 'play']
    nounSyns = ['quiz', 'match', 'game', 'play']
    adjectiveSyns = ['new']
    determinantSyns = ['another']
    tlss = utils.tagAndLemmatizeSentences(message.lower())
    verbs = utils.withoutUselessVerbs(utils.withPOS(tlss, 'VB'))
    nouns = utils.withPOS(tlss, 'NN')
    adjectives = utils.withPOS(tlss, 'JJ')
    determinants = utils.withPOS(tlss, 'DT')
    verbSim = utils.semanticSimilarity(verbs, verbSyns, utils.VERB, 0.2)
    nounSim = utils.semanticSimilarity(nouns, nounSyns, utils.NOUN, 0.2)
    adjectiveSim = utils.semanticSimilarity(adjectives, adjectiveSyns, utils.ADJ, 0.2)
    determinantSim = utils.semanticSimilarity(determinants, determinantSyns, None, 0.2)
    confidence = utils.optimisticMean([verbSim, nounSim, max(adjectiveSim, determinantSim)], weights=[3, 1, 2])
    return confidence, actions.startNewGame


@intent
def dontKnow(user, message):
    # TODO
    return 0, None

@intent
def yes(user, message):
    # TODO
    return 0, None


@intent
def no(user, message):
    # TODO
    return 0, None
