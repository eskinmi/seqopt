import seqopt.optimizers.helpers


class Selector:
    def __call__(self, feed):
        return seqopt.optimizers.helpers.reposition(self.select(feed))


class MaxRelative(Selector):

    def __init__(self, cutoff_ratio, key='score'):
        self.key = key
        self.cutoff = cutoff_ratio

    def select(self, feed):
        _max = max(feed, key=lambda x: x[self.key])[self.key]
        return list(filter(lambda x: x[self.key] >= _max * self.cutoff, feed))


class TopN(Selector):

    def __init__(self, n):
        self.n = n

    def select(self, feed):
        return feed[:self.n]


class AbsoluteThreshold(Selector):

    def __init__(self, threshold, key='score'):
        self.threshold = threshold
        self.key = key

    def select(self, feed):
        return list(filter(lambda x: x[self.key] >= self.threshold, feed))


def do_select(selector, feed):
    if selector is not None:
        return selector(feed)
    else:
        return feed
