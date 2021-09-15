from collections import Counter
import random
from seqopt.optimizers.helpers import reposition_by_index


class Logs:

    def __init__(self, population=None):
        self.initial_population = population
        self.population = self.initial_population
        self.feeds = []
        self.experiment_logs = []
        self.counter = Counter()
        self.feed = None
        self.feed_out = None
        self.items_to_try = None

    def log_feed(self, feed):
        self.feeds.append(feed)
        self.feed = feed
        self.counter.update([i['key'] for i in feed])
        if self.initial_population is None:
            self.population = list(self.counter.keys())

    def log_episode(self, episode, is_opt):
        self.experiment_logs.append({'episode': episode,
                                     'is_opt_episode': is_opt,
                                     'feed': self.feed,
                                     'feed_out': self.feed_out,
                                     'items_added': self.items_to_try
                                     })

    @property
    def unused_items(self):
        if self.initial_population:
            return [item for item in self.population if item not in self.counter.keys()]
        else:
            return []

    def reset_logs(self):
        self.population = self.initial_population
        self.feeds = []
        self.experiment_logs = []
        self.counter = Counter()
        self.feed = None
        self.feed_out = None
        self.items_to_try = None


class Experiments(Logs):

    def __init__(self, population):
        super().__init__(population=population)
        self.episode = 0
        self.experiment_id = 0
        self.logged_experiments = {}

    def add_experiment(self):
        if self.experiment_logs:
            self.logged_experiments[self.experiment_id] = self.experiment_logs

    def reset_experiment(self):
        self.add_experiment()
        self.reset_logs()
        self.episode = 0
        self.experiment_id += 1

    @property
    def experiments(self):
        return {**self.logged_experiments, self.experiment_id : self.experiment_logs}

    @property
    def optimized_seq(self):
        if self.logged_experiments:
            return self.logged_experiments.get(max(self.logged_experiments))[-1].get('feed_out')
        else:
            return self.experiment_logs[-1]['feed_out']


class Trials:

    def __init__(self, n, add_to='last'):
        self.n = n
        if add_to is None:
            self.add_to = 'last'
        else:
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
            return tuple(random.randint(0, n) for _ in range(n))

    def run(self, feed_out, unused_items):
        """
        Add n unused items to the feed, to
            create circular process.
        :param feed_out: experiments.feed_out
        :param unused_items: experiments.unused_items
        :return:
            feed added (list)
        """
        n_add = len(unused_items) if len(unused_items) < self.n else self.n
        items = random.sample(unused_items, n_add)
        indices = self._find_indices_to_add(n_add, length=len(feed_out), add_to=self.add_to)
        return items, self.add_keys(feed_out, items, indices)




