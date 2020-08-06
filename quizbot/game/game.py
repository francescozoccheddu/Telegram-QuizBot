from ..utils import resources

_config = resources.json('game.json')


def scoreIncrement():
    return _config['scoreIncrement']


def giveUpScoreMultiplier():
    return _config['giveUpScoreMultiplier']


def sqCooldownTurns():
    return _config['sqCooldownTurns']


def rwaCooldownTurns():
    return _config['rwaCooldownTurns']


def rwaAnswersCount():
    return _config['rwaAnswersCount']


class Game:

    def __init__(self):
        self._score = None
        self._recordScore = None
        self._oldRecordScore = False
        self._endGame()

    def _endGame(self):
        if self._recordScore is None or self._score > self._recordScore:
            self._oldRecordScore = self._recordScore
            self._recordScore = self._score
        self._question = None
        self._answers = None
        self._rightAnswerIndex = None
        self._sqCooldown = None
        self._rwaCooldown = None
        self._rwaIndices = None
        self._playing = False

    @property
    def isPlaying(self):
        return self._playing

    @property
    def score(self):
        return self._score

    @property
    def recordScore(self):
        return self._recordScore

    @property
    def oldRecordScore(self):
        return self._oldRecordScore

    @property
    def question(self):
        return self._question

    @property
    def answers(self):
        return self._answers

    @property
    def rightAnswerIndex(self):
        return self._rightAnswerIndex

    @property
    def rightAnswer(self):
        return self._answers[self._rightAnswerIndex] if self._playing else None

    @property
    def wrongAnswers(self):
        return [a for i, a in enumerate(self._answers) if i != self._rightAnswerIndex] if self._playing else None

    @property
    def wrongAnwersIndices(self):
        return [i for i in range(len(self._answers)) if i != self._rightAnswerIndex] if self._playing else None

    @property
    def canDoSq(self):
        return self._sqCooldown == 0

    @property
    def canDoRwa(self):
        return self._rwaCooldown == 0

    @property
    def sqCooldown(self):
        return self._sqCooldown

    @property
    def rwaCooldown(self):
        return self._rwaCooldown

    @property
    def rwaIndices(self):
        return self._rwaIndices

    def start(self):
        if self._playing:
            raise Exception('Already playing')
        self._playing = True
        self._score = 0
        self._rwaCooldown = 0
        self._sqCooldown = 0
        self._rwaIndices = tuple()
        self._newQuestion()

    def _newQuestion(self):
        if not self._playing:
            raise Exception('Not playing')
        from ..questions import quizzer
        import random
        question, answers = quizzer.randomQuestion()()
        rightAnswer = answers[0]
        answers = list(answers)
        random.shuffle(answers)
        self._question = question
        self._answers = answers
        self._rightAnswerIndex = answers.index(rightAnswer)
        self._rwaCooldown = max(self._rwaCooldown - 1, 0)
        self._sqCooldown = max(self._sqCooldown - 1, 0)
        self._rwaIndices = tuple()

    def giveUp(self):
        if not self._playing:
            raise Exception('Not playing')
        self._score *= giveUpScoreMultiplier()
        self._endGame()

    def doRwa(self):
        if not self._playing:
            raise Exception('Not playing')
        if not self.canDoRwa:
            raise Exception('Cannot do rwa')
        import random
        self._rwaIndices = tuple(random.sample(self.wrongAnwersIndices, rwaAnswersCount()))
        self._rwaCooldown = rwaCooldownTurns()

    def doSq(self):
        if not self._playing:
            raise Exception('Not playing')
        if not self.canDoSq:
            raise Exception('Cannot do sq')
        self._newQuestion()
        self._sqCooldown = sqCooldownTurns()

    def answer(self, index):
        if not self._playing:
            raise Exception('Not playing')
        if not isinstance(index, int):
            raise TypeError()
        if not (0 <= index < len(self._answers)):
            raise ValueError()
        right = index == self._rightAnswerIndex
        if right:
            self._score += scoreIncrement()
            self._newQuestion()
        else:
            self._endGame()
        return right

    def __getstate__(self):
        return (self._score,
                self._recordScore,
                self._oldRecordScore,
                self._question,
                self._answers,
                self._rightAnswerIndex,
                self._sqCooldown,
                self._rwaCooldown,
                self._rwaIndices,
                self._playing)

    def __setstate__(self, value):
        (self._score,
         self._recordScore,
         self._oldRecordScore,
         self._question,
         self._answers,
         self._rightAnswerIndex,
         self._sqCooldown,
         self._rwaCooldown,
         self._rwaIndices,
         self._playing) = value