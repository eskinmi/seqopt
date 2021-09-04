from seqopt.callbacks import Logs
import random


def _find_indices_from_str(n, add_to):
    if add_to == 'last':
        return tuple(-1 + i for i in range(n))
    elif add_to == 'first':
        return tuple(0 + i for i in range(n))
    elif add_to == 'middle':
        return tuple(round(n) + i for i in range(n))
    else: # random
        return tuple(random.randint(0, n) for i in range(n))


def get_unused_keys(logger: Logs):
    """
    Find keys that are yet unused.
    :param logger: seqopt.callbacks.Logs object
    :return:
        list of keys to add
    """
    return [item for item in logger.population if item not in logger.counter.keys()]


def keys_add(feed, items, indices):
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


class ItemTrials:

    def __init__(self, n, max_items=None, add_to='last'):
        self.n = n
        self.max_items = max_items
        self.add_to = add_to

    @property
    def add_to(self):
        return self._add_to

    @add_to.setter
    def add_to(self, add_to):
        acceptable = ['last', 'first', 'middle', 'random']
        if isinstance(add_to, str) and add_to in acceptable:
            self._add_to = add_to
        else:
            raise ValueError(f"add_to should be one of the following : {', '.join(acceptable)}")

    def add(self, logger: Logs):
        """
        Add n unused items to the feed, to
            create circular process.
        :param logger: seqopt.callbacks.Logs object
        :return:
            feed added (list)
        """
        feed = logger.feeds[-1]
        unused_items = get_unused_keys(logger)
        n_ = len(unused_items) if len(unused_items) < self.n else self.n
        items = random.sample(unused_items, n_)
        indices = _find_indices_from_str(n_, self.add_to)
        feed_added = keys_add(feed, items, indices)
        return feed_added[:self.max_items]
