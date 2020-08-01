from . import quizzer

class Question:

    def __init__(self, producer, topic, difficulty=0.5, datasets=[]):
        if not isinstance(topic, str):
            raise TypeError('Unexpected topic type')
        if not callable(producer):
            raise TypeError('Unexpected producer type')
        if not isinstance(datasets, (list, tuple)) or any(not isinstance(d, str) for d in datasets):
            raise TypeError('Unexpected dataset key type')
        if not isinstance(difficulty, (float, int)):
            raise TypeError('Unexpected difficulty type')
        if 0 > difficulty > 1:
            raise ValueError('Difficulty must fall in range [0,1]')
        self._topic = topic
        self._difficulty = difficulty
        self._producer = producer
        self._datasets = datasets
        quizzer._registerQuestion(self)

    def __call__(self):
        if not self.isReady:
            raise RuntimeError('Not all dependencies are ready')
        return self._producer(*[quizzer._getData(k) for k in self._datasets])

    def __repr__(self):
        return f'{self.__class__.__qualname__}{(self._producer, self._topic, self._difficulty, self._datasets)}'

    def __str__(self):
        return self.producerName

    @property
    def producerName(self):
        return f'{self._producer.__module__}.{self._producer.__qualname__}'

    @property
    def datasetsKeys(self):
        return self._datasets

    @property
    def isReady(self):
        return all(quizzer._getData(dk) is not None for dk in self._datasets)

    def ready(self, onProgress=None):
        if onProgress is not None:
            onProgress(0, len(self._datasets))
        for i, dk in enumerate(self._datasets):
            d = quizzer._getDataset(dk)
            if d is None:
                raise Exception(f'Dataset "{dk}" does not exist')
            d.ready()
            onProgress(i + 1, len(self._datasets))

    @property
    def topic(self):
        return self._topic

    @property
    def difficulty(self):
        return self._difficulty


def question(topic, difficulty=0.5, datasets=[]):
    def wrapper(producer):
        return Question(producer, topic, difficulty, datasets)
    return wrapper
