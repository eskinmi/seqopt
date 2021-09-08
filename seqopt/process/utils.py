import pickle
import random


def load_model(path):
    """
    Load process.
    :param path:
    :return:
    """
    with open(path, 'r') as f:
        model = pickle.load(f)
    return model


def save_model(model, path):
    """
    Checkpoint the process on a given episode.
    :param model: seqopt process.
    :param path: checkpoint location (str)
    """
    with open(f'{path}/process', 'w') as f:
        pickle.dump(model, f)


def _find_indices_from_str(n, length, add_to):
    if add_to == 'last':
        return tuple(length - i for i in range(n))
    elif add_to == 'first':
        return tuple(0 + i for i in range(n))
    elif add_to == 'middle':
        return tuple(round(length/2) + i for i in range(n))
    else: # random
        return tuple(random.randint(0, n) for i in range(n))


def _keys_add(feed, items, indices):
    """
    Add keys to existing feed, in given
        indices.
    :param feed: feed (list)
    :param items: items (iterable)
    :param indices: indices to add (tuple)
    :return:
        feed added (list)
    """

    feed_added = feed.copy()
    items = set([item for item in items if item not in [f['key'] for f in feed_added]])
    for ix, i in enumerate(items):
        feed_added.insert(indices[ix], {'key': i, 'reward': 0, 'pos':ix})
    return feed_added
