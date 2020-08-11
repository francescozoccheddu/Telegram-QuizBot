class Quizzer:

    def __init__(self):
        self._datasets = {}
        self._topics = {}

    @property
    def datasets(self):
        return self._datasets

    @datasets.setter
    def datasets(self, value):
        self._datasets = value

    def registerQuestionFactory(self, factory):
        topic = self._topics.get(factory.topic, set())
        topic.add(factory)
        self._topics[factory.topic] = topic

    def removeQuestionFactory(self, factory):
        topic = self._topics.get(factory.topic, None)
        if topic is not None:
            topic.pop(factory)

    def clearQuestionFactories(self):
        self._topics.clear()

    @property
    def topics(self):
        return tuple(self._topics.keys())

    def questionFactories(self, topics=None, includeNotReady=False):
        if isinstance(topics, str):
            topics = [topics]
        if topics is None or len(topics) == 0:
            return tuple(qf for t in self._topics.values() for qf in t if includeNotReady or qf.isReady)
        else:
            factories = set()
            for t in topics:
                topic = self._topics.get(t, [])
                factories.update(q for q in topic if includeNotReady or q.isReady)
            return tuple(factories)

    def randomQuestion(self, topics=None):
        pool = self.questionFactories(topics)
        if len(pool) == 0:
            return None
        else:
            import random
            question, answers = random.choice(pool)(self.datasets)
            rightAnswer = answers[0]
            answers = list(answers)
            random.shuffle(answers)
            return question, answers, answers.index(rightAnswer)


def registerQuestionFactoriesFromModule(quizzer, module):
    from .questions import QuestionFactory
    for q in module.__dict__.items():
        if isinstance(q, QuestionFactory):
            quizzer.registerQuestion(q)


def makeAutoRegisteringDecorator(quizzer):
    from .questions import QuestionFactory

    def outerWrapper(topic, datasets=[]):
        def innerWrapper(producer):
            q = QuestionFactory(producer, topic, datasets)
            quizzer.registerQuestionFactory(q)
            return q
        return innerWrapper
    return outerWrapper
