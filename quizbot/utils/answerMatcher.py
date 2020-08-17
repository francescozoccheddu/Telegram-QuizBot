def _normalizeText(doc):
    return ' '.join(t.lemma_.lower() for t in doc if t.is_digit or not (t.is_space or t.is_punct or t.is_stop))


def bestBag(answerBags, doc, options):
    import textdistance
    minSim = options.get('minSimilarity', 0.7)
    maxOtherSim = options.get('maxOtherSimilarity', 0.6)
    minOtherSimMargin = options.get('minOtherSimilarityMargin', 0.2)
    bestIndex, best, other = None, 0, 0
    normDoc = _normalizeText(doc)
    for i, answerBag in enumerate(answerBags):
        sim = 0
        for ent in answerBag:
            normEnt = _normalizeText(ent)
            if normEnt and not normEnt.isspace():
                sim = max(textdistance.levenshtein.normalized_similarity(normEnt, normDoc), sim)
        if sim > best:
            other = best
            best = sim
            bestIndex = i
        elif sim > other:
            other = sim
    if best == 1 and other < 1:
        return bestIndex
    if sim < minSim or other > maxOtherSim or best - other < minOtherSimMargin:
        return None
    return bestIndex


def best(answers, doc, options):
    return bestBag(([answer] for answer in answers), doc, options)


def bestWithNER(answers, doc, options):
    bestIndex = best(answers, doc, options)
    answerBags = [list(answer.ents) for answer in answers]
    for ent in doc.ents:
        candidateIndex = bestBag(answerBags, ent, options)
        if bestIndex is None:
            bestIndex = candidateIndex
        elif candidateIndex is not None and candidateIndex != bestIndex:
            return None
    return bestIndex
