from collections import Counter
from . import utils
import random


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
        self.n = 0
        self.runs = {}

    def add_experiment(self):
        self.runs[self.n] = self.logger.logs
        self.n += 1

    @property
    def reset(self):
        if not self.logger.unused_items and self.reset_at_end\
                and self.episodes is not None and self.episode >= self.episodes:
            return True
        else:
            return False

    def log_and_reset(self):
        self.add_experiment()
        self.logger.clear_logs()
        self.episode = 0


class ItemTrials:

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

    def __call__(self, logger: Logs):
        """
        Add n unused items to the feed, to
            create circular process.
        :param logger: seqopt.callbacks.Logs object
        :return:
            feed added (list)
        """
        n_add = self._find_n_add(logger.unused_items)
        items = random.sample(logger.unused_items, n_add)
        indices = utils._find_indices_from_str(n_add, length=len(logger.feed_out), add_to=self.add_to)
        return items, utils._keys_add(logger.feed_out, items, indices)


def do_trial(item_trials: ItemTrials, logger: Logs):
    if item_trials:
        return item_trials(logger)
    else:
        return [], logger.feed_out



