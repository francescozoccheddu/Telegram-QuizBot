
class Question:

    def __init__(self, producer, topic, datasets=[]):
        if not isinstance(topic, str):
            raise TypeError('Unexpected topic type')
        if not callable(producer):
            raise TypeError('Unexpected producer type')
        if not isinstance(datasets, (list, tuple)) or any(not isinstance(d, str) for d in datasets):
            raise TypeError('Unexpected dataset key type')
        self._topic = topic
        self._producer = producer
        self._datasets = datasets

    def __call__(self, datasets):
        if not self.isReady(datasets):
            raise RuntimeError('Not all dependencies are ready')
        return self._producer(*[datasets[k].data for k in self._datasets])

    def __repr__(self):
        return f'{self.__class__.__qualname__}{(self._producer, self._topic, self._datasets)}'

    def __str__(self):
        return self.producerName

    @property
    def producerName(self):
        return f'{self._producer.__module__}.{self._producer.__qualname__}'

    @property
    def datasetsKeys(self):
        return self._datasets

    def isReady(self, datasets):
        def isDatasetReady(key):
            dataset = datasets.get(key)
            return dataset is not None and dataset.isReady
        return all(isDatasetReady(k) for k in self._datasets)

    def ready(self, datasets, onProgress=None):
        if onProgress is not None:
            onProgress(0, len(self._datasets))
        for i, dk in enumerate(self._datasets):
            d = datasets.get(dk)
            if d is None:
                raise Exception(f'Dataset "{dk}" does not exist')
            d.ready()
            onProgress(i + 1, len(self._datasets))

    @property
    def topic(self):
        return self._topic


def question(topic, datasets=[]):
    def wrapper(producer):
        return Question(producer, topic, datasets)
    return wrapper
