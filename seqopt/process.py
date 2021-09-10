from collections import Counter
import random
from seqopt.optimizers.helpers import reposition_by_index


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
                          'items_added': self.items_to_try
                          })

    @property
    def unused_items(self):
        return [item for item in self.population if item not in self.counter.keys()]

    def clear_logs(self):
        self.__init__(self.initial_population)


class Experiments:

    def __init__(self,logger: Logs, episodes=None, reset_at_end=True):
        self.logger = logger
        self.reset_at_end = reset_at_end
        self.episodes = episodes
        self.episode = 0
        self.experiment_id = 0
        self.experiments = {}

    @property
    def output(self):
        if self.experiments:
            return self.experiments.get(max(self.experiments))[-1].get('feed_out')
        else:
            return self.logger.logs[-1]['feed_out']

    def add_experiment(self):
        if self.logger.logs:
            self.experiments[self.experiment_id] = self.logger.logs

    @property
    def to_restart(self):
        if not self.logger.unused_items and self.reset_at_end\
                and not self.episodes:
            return True
        else:
            return False

    def reset_experiment(self):
        self.add_experiment()
        self.logger.clear_logs()
        self.episode = 0
        self.experiment_id += 1


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

    @staticmethod
    def add_keys(feed, items, indices):
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
            feed_added.insert(indices[ix], {'key': i, 'pos': ix, 'reward': 0})
        return reposition_by_index(feed_added)

    @staticmethod
    def _find_indices_to_add(n, length, add_to):
        if add_to == 'last':
            return tuple(length + i for i in range(n))
        elif add_to == 'first':
            return tuple(0 + i for i in range(n))
        elif add_to == 'middle':
            return tuple(round(length / 2) + i for i in range(n))
        else:  # random
            return tuple(random.randint(0, n) for i in range(n))

    def run(self, logger: Logs):
        """
        Add n unused items to the feed, to
            create circular process.
        :param logger: seqopt.callbacks.Logs object
        :return:
            feed added (list)
        """
        n_add = len(logger.unused_items) if len(logger.unused_items) < self.n else self.n
        items = random.sample(logger.unused_items, n_add)
        indices = self._find_indices_to_add(n_add, length=len(logger.feed_out), add_to=self.add_to)
        return items, self.add_keys(logger.feed_out, items, indices)




