def matches(descriptor, doc, falloff=1):
    from spacy.matcher import Matcher
    name = ''
    matcher = Matcher(doc.vocab)
    matches = {}
    for key, intents in descriptor.items():
        visited = [False] * len(doc)
        done = False
        value = 0
        for weight, pattern in intents:
            matcher.add(name, [pattern])
            for _, start, end in matcher(doc):
                if not any(visited[start:end]):
                    value += weight
                    weight *= falloff
                    visited[start:end] = [True] * (end - start)
                    done = all(visited)
                    if done:
                        break
            matcher.remove(name)
            if done:
                break
        matches[key] = value
    return matches


def best(descriptor, doc, options={}):
    import math
    minValue, maxValue = options.get('minValue', -math.inf), options.get('maxValue', math.inf)
    weights = options.get('weights', {})
    maxOtherValue = options.get('maxOtherValue', math.inf)
    minOtherValueMargin = options.get('minOtherValueMargin', -math.inf)
    minBestValue = options.get('minBestValue', -math.inf)
    values = matches(descriptor, doc, options.get('falloff', 1))
    values = {k: min(max(v, minValue), maxValue) for k, v in values.items()}
    values = {k: weights.get(k, 1) * v for k, v in values.items()}
    bestKey, best, other = None, -math.inf, -math.inf
    for k, v in values.items():
        if v > best:
            other = best
            best = v
            bestKey = k
        elif v > other:
            other = v
    if best < minBestValue or other > maxOtherValue or best - other < minOtherValueMargin:
        return None
    else:
        return bestKey
