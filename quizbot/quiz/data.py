
_datasets = None

def readyAllDatasets(output=True):
    def onFailure(key, error):
        output(f'Exception while processing dataset "{key}": {error}')
    if output:
        def plural(n):
            return 's' if n != 1 else ''
        if _datasets is None or reloadDescriptors:
            print('Loading datasets descriptors...')
            loadDatasets()
            ready = sum(1 for d in _datasets.values() if d.isReady)
            readyMessage = f' ({ready} dataset{plural(ready)} from cache)' if ready > 0 else ''
            print(f'Done loading {len(_datasets)} dataset descriptor{plural(len(_datasets))}{readyMessage}.')
        print('Collecting datasets... (This may take minutes)')
        try:
            from tqdm import tqdm
        except ImportError:
            onProgress = None
            output = print
            bar = None
        else:
            bar = tqdm(total=None, bar_format='{percentage:3.0f}% |{bar}| {n_fmt}/{total_fmt}')

            def onProgress(p, t):
                bar.total = t
                bar.n = p
                bar.refresh()
            output = tqdm.write
        readyAllDatasets(onProgress, onFailure)
        if bar is not None:
            bar.close()
        nonready = sum(1 for d in _datasets.values() if not d.isReady)
        failsMessage = ' All datasets are ready.' if nonready == 0 else f' (Failed to collect {nonready} dataset{plural(nonready)}'
        print(f'Done.{failsMessage}')
        print('Caching datasets...')
        cacheDatasets()
        print('Done.')
    else:
        if _datasets is None or reloadDescriptors:
            loadDatasets()
        readyAllDatasets(onFailure=onFailure)
        cacheDatasets()


def loadDatasets():
    from . import datasets
    filename = _config['datasetsFile']
    global _datasets
    _datasets = datasets.fromResource(filename, lambda t: '/'.join(t), _config['datasetsCacheFile'])


def cacheDatasets():
    from . import datasets
    datasets.cache(_datasets, _config['datasetsCacheFile'])


def readyAllDatasets(onProgress=None, onFailure=None):
    datasets = list((k, d) for k, d in _datasets.items() if not d.isReady)
    if onProgress is not None:
        onProgress(0, len(datasets))
    for i, t in enumerate(datasets):
        k, d = t
        try:
            d.ready()
        except Exception as e:
            if onFailure is not None:
                onFailure(k, e)
        if onProgress is not None:
            onProgress(i + 1, len(datasets))


def getDataset(key):
    return _datasets.get(key, None) if _datasets is not None else None


def getData(key):
    dataset = _getDataset(key)
    if dataset is None or not dataset.isReady:
        return None
    return dataset.data
