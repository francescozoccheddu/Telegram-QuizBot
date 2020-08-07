from ..actions import base, lifelines, confirm
from . import utils
from autocorrect import Speller

_speller = Speller()


def fallback(user, message):
    return 0.5, base.didntUnderstandAction


def giveUp(user, message):
    verbSyns = ['quit', 'stop', 'abandon', 'surrender', 'leave', 'give up']
    tlss = utils.tagAndLemmatizeSentences(_speller(message).lower(), [('give', 'up')])
    verbs = utils.withPOS(tlss, 'VB')
    singletons = utils.singleWordSentences(tlss)
    candidates = utils.withoutUselessVerbs(verbs + singletons)
    confidence = utils.semanticSimilarity(candidates, verbSyns, utils.VERB, 0)
    return confidence, base.giveUp


def switchQuestion(user, message):
    verbSyns = ['change', 'switch', 'replace', 'swap']
    nounSyns = ['question', 'quiz']
    adjectiveSyns = ['new', 'different']
    determinantSyns = ['another']
    tlss = utils.tagAndLemmatizeSentences(_speller(message).lower())
    verbs = utils.withoutUselessVerbs(utils.withPOS(tlss, 'VB'))
    nouns = utils.withPOS(tlss, 'NN')
    adjectives = utils.withPOS(tlss, 'JJ')
    determinants = utils.withPOS(tlss, 'DT')
    verbSim = utils.semanticSimilarity(verbs, verbSyns, utils.VERB, 0.2)
    nounSim = utils.semanticSimilarity(nouns, nounSyns, utils.NOUN, 0.2)
    adjectiveSim = utils.semanticSimilarity(adjectives, adjectiveSyns, utils.ADJ, 0.2)
    determinantSim = utils.semanticSimilarity(determinants, determinantSyns, None, 0.2)
    confidence = utils.optimisticMean([verbSim, nounSim, max(adjectiveSim, determinantSim)], weights=[2, 1, 1])
    return confidence, lifelines.doSq


def removeTwoWrongQuestions(user, message):
    verbSyns = ['remove', 'delete', 'hide']
    nounSyns = ['answer', 'response']
    adjectiveSyns = ['wrong', 'incorrect']
    numberSyns = ['two']
    tlss = utils.tagAndLemmatizeSentences(_speller(message).lower())
    verbs = utils.withoutUselessVerbs(utils.withPOS(tlss, 'VB'))
    nouns = utils.withPOS(tlss, 'NN')
    adjectives = utils.withPOS(tlss, 'JJ')
    numbers = utils.withPOS(tlss, 'CD')
    verbSim = utils.semanticSimilarity(verbs, verbSyns, utils.VERB, 0.2)
    nounSim = utils.semanticSimilarity(nouns, nounSyns, utils.NOUN, 0.2)
    adjectiveSim = utils.semanticSimilarity(adjectives, adjectiveSyns, utils.ADJ, 0.2)
    numberSim = utils.semanticSimilarity(numbers, numberSyns, None, 0.2)
    confidence = utils.optimisticMean([verbSim, nounSim, adjectiveSim, numberSim], weights=[3, 1, 2, 0.5])
    return confidence, lifelines.doRwa


def hint(user, message):
    nounSyns = ['help', 'hint', 'aid']
    tlss = utils.tagAndLemmatizeSentences(_speller(message).lower())
    nouns = utils.withPOS(tlss, 'NN')
    confidence = utils.semanticSimilarity(nouns, nounSyns, utils.NOUN, 0)
    return confidence, lifelines.doRwa


def startGame(user, message):
    verbSyns = ['start', 'begin', 'play']
    nounSyns = ['quiz', 'match', 'game', 'play']
    adjectiveSyns = ['new']
    determinantSyns = ['another']
    tlss = utils.tagAndLemmatizeSentences(_speller(message).lower())
    verbs = utils.withoutUselessVerbs(utils.withPOS(tlss, 'VB'))
    nouns = utils.withPOS(tlss, 'NN')
    adjectives = utils.withPOS(tlss, 'JJ')
    determinants = utils.withPOS(tlss, 'DT')
    verbSim = utils.semanticSimilarity(verbs, verbSyns, utils.VERB, 0.2)
    nounSim = utils.semanticSimilarity(nouns, nounSyns, utils.NOUN, 0.2)
    adjectiveSim = utils.semanticSimilarity(adjectives, adjectiveSyns, utils.ADJ, 0.2)
    determinantSim = utils.semanticSimilarity(determinants, determinantSyns, None, 0.2)
    confidence = utils.optimisticMean([verbSim, nounSim, max(adjectiveSim, determinantSim)], weights=[3, 2, 1])
    return confidence, base.startNewGame


_yesNoIgnoreWords = {'i', 'i\'m', 'am', 'please', 'do'}
_yesNoIgnoreBow = utils.constantCostBow(_yesNoIgnoreWords, 0)


def yes(user, message):
    confidence = utils.bowSimilarity(_speller(message), {
        'yes': 1,
        'sure': 1,
        'ok': 1,
        'no': -2,
        'not': -2,
        'n\'t': -2,
        **_yesNoIgnoreBow
    }, -0.3)
    return confidence, confirm.yesNo, True


def no(user, message):
    confidence = utils.bowSimilarity(_speller(message), {
        'yes': -2,
        'sure': -2,
        'ok': -2,
        'no': 1,
        'not': 1,
        'n\'t': 1,
        **_yesNoIgnoreBow
    }, -0.3)
    return confidence, confirm.yesNo, False


_cardinalAnswerIgnoreWords = {'i', 'i\'m', 'am', 'please', 'do', 'sure', 'choose', 'answer', 'one', 'choice', 'number'}
_cardinalAnswerIgnoreBow = utils.constantCostBow(_cardinalAnswerIgnoreWords, 0)
_firstAnswerWords = {'first', '1st', '1'}
_secondAnswerWords = {'second', '2nd', 'two', '2'}
_thirdAnswerWords = {'third', '3rd', 'three', '3'}
_fourthAnswerWords = {'fourth', '4th', 'four', '4'}
_answerWords = [_firstAnswerWords, _secondAnswerWords, _thirdAnswerWords, _fourthAnswerWords]


def answerByIndex(user, message):
    tlss = utils.tagAndLemmatizeSentences(_speller(message))
    confidence, index = 0, 0
    for i in range(len(_answerWords)):
        s = utils.bowSimilarity(tlss, {
            **utils.constantCostBow([w for a in _answerWords[:i] for w in a], -2),
            **utils.constantCostBow(_answerWords[i], 1),
            **utils.constantCostBow([w for a in _answerWords[i + 1:] for w in a], -2),
            **_cardinalAnswerIgnoreBow
        }, -0.3)
        if s > confidence:
            confidence = s
            index = i
    return confidence, base.answer, index
