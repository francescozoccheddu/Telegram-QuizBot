def separatorKeyProvider(separator='/'):
    return lambda t: separator.join(t)


def loadAndReady(descriptorFileOrDatasets, keyProvider=separatorKeyProvider(), cacheFile=None, output=True, outputFailures=True):
    from .datasets import fromResource, cache
    from ..utils import nlg
    if isinstance(descriptorFileOrDatasets, str):
        if output:
            print('Loading datasets descriptors...')
        datasets = fromResource(descriptorFileOrDatasets, keyProvider, cacheFile)
        if output:
            ready = sum(1 for d in datasets.values() if d.isReady)
            readyMessage = f' ({ready} dataset{nlg.plur(ready)} from cache)' if ready > 0 else ''
            print(f'Done loading {len(datasets)} dataset descriptor{nlg.plur(datasets)}{readyMessage}.')
    else:
        datasets = descriptorFileOrDatasets
    readyDatasets(datasets, output=output, outputFailures=outputFailures)
    if cacheFile is not None:
        if output:
            print('Caching datasets...')
        cache(datasets, cacheFile)
        if output:
            print('Caching done.')
    return datasets


def readyDatasets(datasets, output=True, outputFailures=True):
    datasets = list((k, d) for k, d in datasets.items() if not d.isReady)
    from ..utils.nlg import plur
    bar = None
    write = print
    if len(datasets) > 0:
        if output:
            try:
                from tqdm import tqdm
            except ImportError:
                pass
            else:
                bar = tqdm(total=len(datasets), bar_format='{percentage:3.0f}% |{bar}| {n_fmt}/{total_fmt}')
                write = tqdm.write
        if output:
            write(f'Collecting {len(datasets)} dataset{plur(datasets)}. (This may take minutes)')
            if bar is None:
                write(' Please wait...')
        for k, d in datasets:
            try:
                d.ready()
            except Exception as e:
                if outputFailures:
                    write(f'Exception while processing dataset "{k}": {e}')
            if bar is not None:
                bar.update()
        if bar is not None:
            bar.close()
    if output:
        nonready = sum(1 for t in datasets if not t[1].isReady)
        write(f'Done. ' + 'All datasets are ready.' if nonready == 0 else f'(Failed to collect {nonready} dataset{plur(nonready)}')
