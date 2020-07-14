from enum import Enum, auto


class Tag(Enum):
    log = auto()
    warning = auto()
    error = auto()


class Mode(Enum):
    manual = auto()
    step = auto()
    split = auto()


class Task:

    def __init__(self, parent, name):
        self._cachedProgress = 0
        self._progress = None
        self._parent = parent
        self._name = name

    def _changeCachedProgress(self, value):
        changed = value != self._cachedProgress
        self._cachedProgress = value
        return changed

    def _calculateProgress(self):
        mode = self.mode
        if mode == Mode.manual:
            return self._progress
        elif mode == Mode.step:
            p, t = self._progress
            return p / t
        elif mode == Mode.split:
            p = 0
            for t, w in self._progress:
                p += t._cachedProgress * w
            return min(p, 1)
        else:
            return 0

    def _updateParentProgress(self):
        parent = self._parent
        while parent is not None:
            if isinstance(parent, TaskHolder):
                parent._progressUpdated()
                break
            if not parent._changeCachedProgress(parent._calculateProgress()):
                break
            parent = parent._parent

    def _update(self):
        if self._changeCachedProgress(self._calculateProgress()):
            self._updateParentProgress()

    @property
    def name(self):
        return self._name

    @property
    def parent(self):
        return self._parent

    def message(self, message, tag):
        parent = self
        tree = []
        while parent is not None:
            if isinstance(parent, TaskHolder):
                parent._message(message, tag, tree)
                break
            tree = [parent] + tree
            parent = parent._parent

    def log(self, message):
        self.message(message, Tag.log)

    def warn(self, message):
        self.message(message, Tag.warning)

    def error(self, message):
        self.message(message, Tag.error)

    @property
    def mode(self):
        if isinstance(self._progress, (int, float)):
            return Mode.manual
        elif isinstance(self._progress, list):
            return Mode.split
        elif isinstance(self._progress, tuple):
            return Mode.step

    @property
    def progress(self):
        return self._cachedProgress

    @progress.setter
    def progress(self, value):
        if self.mode not in (Mode.manual, None):
            raise Exception('Not in manual mode')
        if value < 0 or value > 1:
            raise ValueError('Progress does not fall in range [0,1]')
        self._progress = value
        self._update()

    def clear(self):
        if self.mode == Mode.split:
            for t in self._progress:
                t._parent = None
        self._progress = None

    @property
    def step(self):
        if self.mode != Mode.step:
            raise Exception('Not in step mode')
        return self._progress[0]

    @step.setter
    def step(self, value):
        if self.mode != Mode.step:
            raise Exception('Not in step mode')
        if value < 0 or value > self._progress[1]:
            raise ValueError(f'Step does not fall in range [0,{self.stepCount}')
        self._progress = (value, self._progress[1])
        self._update()

    @property
    def stepCount(self):
        if self.mode != Mode.step:
            raise Exception('Not in step mode')
        return self._progress[1]

    @stepCount.setter
    def stepCount(self, value):
        mode = self.mode
        if mode not in (Mode.step, None):
            raise Exception('Not in step mode')
        if value < 1:
            raise Exception('Step count must be positive')
        if mode is not None and value < self.step:
            raise Exception('Step count must be greater than actual step')
        if mode == Mode.step:
            self._progress = (self._progress[0], value)
        else:
            self._progress = (0, value)
        self._update()

    def nextStep(self):
        self.step += 1

    def done(self):
        mode = self.mode
        if mode == Mode.step:
            self.step = self.stepCount
        elif mode == Mode.split:
            raise Exception('Cannot directly set the progress of a split task')
        else:
            self.progress = 1

    def split(self, count=None, weights=None, names=None):
        if self.mode is not None:
            raise Exception('Mode is not None')
        if (count, weights, names) == (None, None, None):
            raise ValueError('At least one parameter is required')
        count = count if count is not None else len(weights) if weights is not None else len(names)
        if (weights is not None and len(weights) != count) or (names is not None and len(names) != count):
            raise ValueError('Inconsistent list lengths')
        if weights is None:
            w = 1 / count
            weights = [w] * count
        else:
            if not all(isinstance(w, (int, float)) for w in weights):
                raise TypeError('Weight must be float or int')
            total = sum(weights)
            weights = [w / total for w in weights]
        if names is None:
            names = [None] * count
        elif not all(isinstance(n, str) for n in names):
            raise TypeError('Name must be str')
        subtasks = [Task(self, n) for n in names]
        self._progress = list(zip(subtasks, weights))
        self._update()
        return subtasks

    def __repr__(self):
        mode = self.mode
        return f'<{self.__class__.__qualname__}, name="{self._name}", mode={mode.name if mode else None}, progress={self.progress}>'

    def __str__(self):
        return f'{self._name} ({int(round(self.progress * 100))}%)'


class TaskHolder:

    def __init__(self, name=None):
        self._progressCallback = None
        self._messageCallback = None
        self._task = Task(self, name)

    def _message(self, message, tag, tree):
        if self._messageCallback is not None:
            self._messageCallback(self, message, tag, tree)

    def _progressUpdated(self):
        if self._progressCallback is not None:
            self._progressCallback(self)

    @property
    def progressCallback(self):
        return self._progressCallback

    @progressCallback.setter
    def progressCallback(self, callback):
        self._progressCallback = callback

    @property
    def messageCallback(self):
        return self._messageCallback

    @messageCallback.setter
    def messageCallback(self, callback):
        self._messageCallback = callback

    @property
    def name(self):
        return self._task._name

    @property
    def task(self):
        return self._task

    @property
    def progress(self):
        return self._task.progress

    @property
    def percentage(self):
        return int(round(self.progress * 100))

    def __repr__(self):
        return f'<{self.__class__.__qualname__}, name="{self._task._name}", progress={self.progress}>'

    def __str__(self):
        return f'{self._task._name} ({self.percentage}%)'


def ui(func, taskName=None):
    holder = TaskHolder(taskName)
    try:
        from tqdm import tqdm
        bar = tqdm(total=100, bar_format='{percentage:3.0f}% |{bar}|')

        def progressCallback(_):
            bar.update(holder.percentage - bar.n)

        holder.progressCallback = progressCallback
        output = tqdm.write
    except ImportError:
        bar = None
        output = print
        print('Please wait...')

    def messageCallback(_, msg, tag, tree):
        tree = '>'.join(map(lambda t: t.name or '?', tree))
        output(f'[{tag.name if isinstance(tag, Tag) else tag}@{tree}] {msg}')

    holder.messageCallback = messageCallback
    try:
        func(holder.task)
    finally:
        if bar is not None:
            bar.close()
        output('Done.')
