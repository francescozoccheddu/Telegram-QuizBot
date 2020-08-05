from nltk.tokenize import sent_tokenize, word_tokenize, MWETokenizer
from nltk.tag import pos_tag
from nltk.corpus import wordnet, stopwords
from nltk.stem import WordNetLemmatizer
import re

_lemmatizer = WordNetLemmatizer()
_stopWords = set(stopwords.words('english'))
_singleWordRegex = re.compile(r'^(VB|NN|JJ|CD)[A-Z]*$')

ADJ = wordnet.ADJ
ADJ_SAT = wordnet.ADJ_SAT
ADV = wordnet.ADV
VERB = wordnet.VERB
NOUN = wordnet.NOUN


def _semanticSimilarity(a, b):
    if a == b:
        return 1
    else:
        return a.wup_similarity(b)


def _tb2wnPos(tag):
    if tag.startswith('J'):
        return ADJ
    elif tag.startswith('V'):
        return VERB
    elif tag.startswith('N'):
        return NOUN
    elif tag.startswith('R'):
        return ADV
    else:
        return None


def _lemmatize(w, tbt):
    wnTag = _tb2wnPos(tbt)
    if wnTag is None:
        return w
    else:
        return _lemmatizer.lemmatize(w, wnTag)


def _synset(w, pos=None):
    try:
        s = wordnet.synsets(w.replace(' ', '_'), pos)
        return s[0] if len(s) > 0 else None
    except:
        return None


def tagAndLemmatizeWords(words):
    taggedWords = pos_tag(words)
    return [(_lemmatize(w, t), t) for (w, t) in taggedWords]


def tagAndLemmatizeSentences(sentences, multiwords=[]):
    wordTokenizer = MWETokenizer(multiwords)
    ss = [word_tokenize(s) for s in sent_tokenize(sentences)]
    ss = [wordTokenizer.tokenize(s) for s in ss]
    return [tagAndLemmatizeWords(s) for s in ss]


def average(l):
    return sum(l) / max(len(l), 1)


def lerp(a, b, p):
    return a * (1 - p) + b * p


def optimisticMean(l, min=0.25, ifEmpty=None):
    if len(l) == 0:
        return ifEmpty
    m = max(l)
    vsum, wsum = 0, 0
    for v in l:
        if v < 0:
            raise ValueError('Negative values are not allowed')
        w = min + (v / m) * (1 - min)
        vsum += v * w
        wsum += w
    return vsum / wsum


def semanticSimilarity(a, b, pos=None, default=None):
    from collections.abc import Iterable
    if not isinstance(a, Iterable):
        a = [a]
    if not isinstance(b, Iterable):
        b = [b]
    sa = set(notNone(_synset(w, pos) for w in a))
    sb = set(notNone(_synset(w, pos) for w in b))
    sss = []
    for a in sa:
        ss = []
        for b in sb:
            s = _semanticSimilarity(a, b)
            if s is not None:
                ss.append(s)
        if len(ss) > 0:
            sss.append(optimisticMean(ss))
    return optimisticMean(sss, ifEmpty=default)


def singleWordSentences(sentences, syns, pos=None, default=None):
    import string
    ms = []
    for ts in sentences:
        ws = [w for (w, t) in ts if w not in _stopWords and w not in string.punctuation and _singleWordRegex.match(t)]
        if len(ws) == 1:
            ms += ws
    return ms


def notNone(l):
    return [i for i in l if i is not None]
