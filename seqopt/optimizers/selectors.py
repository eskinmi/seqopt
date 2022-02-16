import seqopt.optimizers.helpers
from abc import ABC, abstractmethod


class Selector(ABC):
    """
    Selector main class.
    """
    @abstractmethod
    def select(self):
        pass

    def apply(self, feed):
        return seqopt.optimizers.helpers.reposition(self.select(feed))


class MaxRelative(Selector):
    """
    Makes selection based on the cutoff value
        relative to the max score in scored feed.

        :param cutoff_ratio: cutoff_ratio (int/float)
        :param key: key to apply the rule on (str)
    """
    def __init__(self, cutoff_ratio, key='score'):
        super().__init__()
        self.key = key
        self.cutoff = cutoff_ratio

    def select(self, feed):
        _max = max(feed, key=lambda x: x[self.key])[self.key]
        return list(filter(lambda x: x[self.key] >= _max * self.cutoff, feed))


class TopN(Selector):
    """
    Selects top n items in the scored feed.
        :param n: number of items (int)
    """

    def __init__(self, n):
        self.n = n
        super().__init__()

    def select(self, feed):
        return feed[:self.n]


class AbsoluteThreshold(Selector):
    """
    Makes selection based on the a constant
        (an absolute threshold).

        :param threshold: threshold (int/float)
        :param key: key to apply the rule on (str)
    """
    def __init__(self, threshold, key='score'):
        super().__init__()
        self.threshold = threshold
        self.key = key

    def select(self, feed):
        return list(filter(lambda x: x[self.key] >= self.threshold, feed))


def do_select(selector, feed):
    if selector is not None:
        return selector(feed)
    else:
        return feed
