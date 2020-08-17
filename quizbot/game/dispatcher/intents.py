from . import utils
from ...utils.resources import LazyJson

_speller = None
_nlp = None
_actions = None
_fallbackAction = None
_answerActionKey = 'answer'
_config = LazyJson('configs/gameIntents.json')
_matcherDescriptor = None


def _load():
    import spacy
    from spacy.matcher import Matcher
    from ...utils import resources
    from autocorrect import Speller
    from ..actions import base, lifelines, confirm, remind
    global _nlp, _speller, _actions, _fallbackAction, _matcherDescriptor
    _nlp = spacy.load(_config.spacyDataset)
    _speller = Speller()
    _matcherDescriptor = resources.json('other/gameIntents.json')
    _actions = {
        'newGame': base.startNewGame,
        'giveUp': base.giveUp,
        'no': lambda u: confirm.yesNo(u, False),
        'yes': lambda u: confirm.yesNo(u, True),
        'score': remind.score,
        'record': remind.recordScore,
        'question': remind.question,
        'lifelines': remind.lifelines,
        'doRwa': lifelines.doRwa,
        'doSq': lifelines.doSq,
        'help': remind.help,
        _answerActionKey: base.answer
    }
    _fallbackAction = base.didntUnderstand


_load()


def _extractAnswerIndex(userData, doc):
    g = userData
    if g.isPlaying:
        from ...utils import nlg
        answersCount = len(g.answers)
        candidate = None
        for t in doc:
            card = nlg.invCard(t.lemma_)
            isCard = card is not None and 1 <= card <= answersCount
            ord = nlg.invOrd(t.lemma_)
            isOrd = ord is not None and 1 <= ord <= answersCount
            nextT = t.nbor(1).lemma_ if len(doc) > t.i + 1 else None
            prevT = t.nbor(-1).lemma_ if t.i > 0 else None
            isNumber = False
            isNumber |= isOrd and nextT in ['answer', 'choice', 'one']
            isNumber |= isCard and prevT in ['answer', 'number', 'choice']
            isNumber |= (isCard or isOrd) and sum(1 for ot in doc if nlg.invNum(ot.lemma_) is not None) == 1
            if isNumber:
                number = nlg.invNum(t.text)
                if number is not None:
                    index = number - 1
                    if 0 <= index < answersCount:
                        if candidate is None or candidate == index:
                            candidate = index
                        else:
                            return None
        return candidate if candidate is not None else None
    else:
        return None


def _getActionWeights(userData, validAnswerIndex=True):
    g = userData
    wp = _config.wrongPlayingStateWeight
    uc = _config.unexpectedConfirmWeight
    ul = _config.unavailableLifelineWeight
    ia = _config.invalidAnswerIndexWeight
    return {
        'newGame': 1 if not g.isPlaying else wp,
        'giveUp': 1 if g.isPlaying else wp,
        'no': 1 if g.hasYesNoAction else uc,
        'yes': 1 if g.hasYesNoAction else uc,
        'question': 1 if g.isPlaying else wp,
        'lifelines': 1 if g.isPlaying else wp,
        'doRwa': 1 if g.canDoRwa else ul if g.isPlaying else wp,
        'doSq': 1 if g.canDoSq else ul if g.isPlaying else wp,
        'help': 1,
        _answerActionKey: 1 if validAnswerIndex else ia
    }


def _extractStaticMatcherAction(userData, doc):
    from ...utils import intentMatcher
    answerIndex = _extractAnswerIndex(userData, doc)
    options = {
        'weights': _getActionWeights(userData, answerIndex is not None),
        'minValue': _config.staticMinValue,
        'maxValue': _config.staticMaxValue,
        'minBestValue': _config.staticMinBestValue,
        'maxOtherValue': _config.staticMaxOtherValue,
        'minOtherValueMargin': _config.staticMinOtherValueMargin,
        'falloff': _config.staticFalloff
    }
    bestKey = intentMatcher.best(_matcherDescriptor, doc, options)
    if bestKey == _answerActionKey:
        if answerIndex is None:
            bestKey = None
    return bestKey, answerIndex


def _extractDirectAnswerActionIndex(userData, doc):
    g = userData
    if g.isPlaying:
        from ...utils import answerMatcher
        options = {
            'minSimilarity': _config.directMinSimilarity,
            'maxOtherSimilarity': _config.directMaxOtherSimilarity,
            'minOtherSimilarityMargin': _config.directminOtherSimilarityMargin
        }
        answers = [_nlp(answer) for answer in g.answers]
        return answerMatcher.bestWithNER(answers, doc, options)
    else:
        return None


def process(user, message):
    if _config.autocorrect:
        message = _speller(message)
    doc = _nlp(message)
    answerIndex = _extractDirectAnswerActionIndex(user.data, doc)
    if answerIndex is None:
        actionKey, answerIndex = _extractStaticMatcherAction(user.data, doc)
    else:
        actionKey = _answerActionKey
    args = [answerIndex] if actionKey == _answerActionKey else []
    action = _actions.get(actionKey, _fallbackAction)
    action(user, *args)
