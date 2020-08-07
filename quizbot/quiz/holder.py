class Holder:

    def __init__(self):
        self._datasets = {}
        self._topics = {}

    @property
    def datasets(self):
        return self._datasets

    @datasets.setter
    def datasets(self, value):
        self._datasets = value

    def registerQuestion(self, question):
        topic = self._topics.get(question.topic, set())
        topic.add(question)
        self._topics[question.topic] = topic

    def removeQuestion(self, question):
        topic = self._topics.get(question.topic, None)
        if topic is not None:
            topic.pop(question)

    def clearQuestions(self):
        self._topics.clear()

    @property
    def topics(self):
        return tuple(self._topics.keys())

    def questions(self, topics=None, includeNotReady=False):
        if isinstance(topics, str):
            topics = [topics]
        if topics is None or len(topics) == 0:
            return tuple(q for t in self._topics.values() for q in t if includeNotReady or q.isReady)
        else:
            questions = set()
            for t in topics:
                topic = self._topics.get(t, [])
                questions.update(q for q in topic if includeNotReady or q.isReady)
            return tuple(questions)

    def randomQuestion(self, topics=None, includeNotReady=False):
        pool = self.questions(topics, includeNotReady)
        if len(pool) == 0:
            return None
        else:
            import random
            return random.choice(pool)
