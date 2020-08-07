from nltk.tokenize import sent_tokenize, word_tokenize, MWETokenizer
from nltk.tag import pos_tag
from nltk.corpus import wordnet, stopwords
from nltk.stem import WordNetLemmatizer
from nltk.metrics.distance import edit_distance
import re
import string

_lemmatizer = WordNetLemmatizer()
_stopWords = set(stopwords.words('english')) | set(string.punctuation)
_singleWordRegex = re.compile(r'^(VB|NN|JJ|CD)[A-Z]*$')
_multipleSpacesRegex = re.compile(r'\s+')

uselessVerbs = ['want', 'please', 'do', 'like', 'will', 'would', 'think', 'am']

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
    return [(_lemmatize(w, t), t) for w, t in taggedWords]


def tagAndLemmatizeSentences(sentences, multiwords=[]):
    wordTokenizer = MWETokenizer(multiwords)
    ss = [word_tokenize(s) for s in sent_tokenize(sentences)]
    ss = [wordTokenizer.tokenize(s) for s in ss]
    return [tagAndLemmatizeWords(s) for s in ss]


def average(l):
    return sum(l) / max(len(l), 1)


def lerp(a, b, p):
    return a * (1 - p) + b * p


def weightedMean(l, w):
    vsum, wsum = 0, 0
    for v, w in zip(l, w):
        vsum += v * w
        wsum += w
    return vsum / wsum


def optimisticMean(l, min=0.25, weights=None, ifEmpty=None):
    if len(l) == 0:
        return ifEmpty
    m = max(l)
    w = [min + (v / m) * (1 - min) for v in l]
    if weights is not None:
        for i in range(len(w)):
            w[i] *= weights[i]
    return weightedMean(l, w)


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


def singleWordSentences(sentences):
    import string
    ms = []
    for ts in sentences:
        ws = [w for w, t in ts if w not in _stopWords and _singleWordRegex.match(t)]
        if len(ws) == 1:
            ms += ws
    return ms


def notNone(l):
    return [i for i in l if i is not None]


def withoutUselessVerbs(words):
    return [w for w in words if semanticSimilarity(w, uselessVerbs, pos=VERB, default=0) < 0.5]


def withPOS(taggedWords, pos):
    if len(taggedWords) > 0 and isinstance(taggedWords[0], list):
        return list(*(withPOS(s, pos) for s in taggedWords))
    return [w for w, t in taggedWords if t.startswith(pos)]


def normalize(message):
    return ' '.join(w for w in word_tokenize(message.lower()) if w not in _stopWords)


def editSimilarity(a, b):
    a = normalize(a)
    b = normalize(b)
    return max(1 - (edit_distance(a, b) / max(1, len(a), len(b))), 0)


def bowSimilarity(words, bow, default):
    import string
    bow = dict((w.strip().lower(), c) for w, c in bow.items())
    if isinstance(words, str):
        tlss = tagAndLemmatizeSentences(words)
    else:
        tlss = words
    tws = [w.strip().lower() for s in tlss for w, t in s if w.strip().lower() in bow or w not in _stopWords]
    sim = 0
    for w in tws:
        sim += bow.get(w, default)
    return min(max(sim, 0), 1)


def constantCostBow(words, cost):
    return dict(zip(words, [cost] * len(words)))
