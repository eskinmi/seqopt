from collections import Counter
import random


def _find_indices(n, length, add_to):
    if add_to == 'last':
        return tuple(length - i for i in range(n))
    elif add_to == 'first':
        return tuple(0 + i for i in range(n))
    elif add_to == 'middle':
        return tuple(round(length/2) + i for i in range(n))
    else: # random
        return tuple(random.randint(0, n) for i in range(n))


def _add_keys(feed, items, indices):
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


class Logs:

    def __init__(self, population=None):
        self.initial_population = population
        self.population = self.initial_population
        self.feeds = []
        self.logs = []
        self.counter = Counter()
        self.feed = None
        self.feed_out = None
        self.items_to_try=None

    def log_feed(self, feed):
        self.feeds.append(feed)
        self.feed = feed
        self.counter.update([i['key'] for i in feed])
        if self.initial_population is None:
            self.population = list(self.counter.keys())

    def log_episode(self, episode, is_opt):
        self.logs.append({'episode': episode,
                          'is_opt_episode': is_opt,
                          'feed': self.feed,
                          'feed_out': self.feed_out,
                          'items_added' : self.items_to_try
                          })

    @property
    def unused_items(self):
        return [item for item in self.population if item not in self.counter.keys()]

    def clear_logs(self):
        self.__init__(self.initial_population)


class Experiments:

    def __init__(self,
                 logger: Logs,
                 episodes=None,
                 reset_at_end=True,
                 ):
        self.logger = logger
        self.reset_at_end = reset_at_end
        self.episodes = episodes
        self.episode = 0
        self.experiment_id = 0
        self.experiments = {}

    def add_experiment(self):
        self.experiments[self.experiment_id] = self.logger.logs

    @property
    def reset(self):
        reset_now = False
        if not self.logger.unused_items and self.reset_at_end:
            if not self.episodes:
                reset_now = True
        return reset_now


class Trials:

    def __init__(self, n, add_to='last'):
        self.n = n
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

    def _find_n_add(self, unused_items):
        return len(unused_items) if len(unused_items) < self.n else self.n

    def run(self, logger: Logs):
        """
        Add n unused items to the feed, to
            create circular process.
        :param logger: seqopt.callbacks.Logs object
        :return:
            feed added (list)
        """
        n_add = self._find_n_add(logger.unused_items)
        items = random.sample(logger.unused_items, n_add)
        indices = _find_indices(n_add, length=len(logger.feed_out), add_to=self.add_to)
        return items, _add_keys(logger.feed_out, items, indices)



