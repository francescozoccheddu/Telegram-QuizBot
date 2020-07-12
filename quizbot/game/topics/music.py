from ..quiz import Topic, question, answerCount
from ...utils import range, sparql, easing
import random

topic = Topic('music')

_querier = sparql.Querier(sparql.dbpediaEndpointUrl)


@question(topic)
def whoMadeThisSong(difficulty):
    pass

@question(topic)
def whatSongDidTheyDo(difficulty):
    pass

@question(topic)
def whatBandAreTheyIn(difficulty):
    pass

@question(topic)
def whoMadeThisAlbum(difficulty):
    pass

@question(topic)
def whatSongCameOutEarlier(difficulty):
    pass
