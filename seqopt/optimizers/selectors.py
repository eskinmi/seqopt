
class MaxRelative:

    def __init__(self, cutoff_ratio, key='score'):
        self.key = key
        self.cutoff = cutoff_ratio

    def __call__(self, feed):
        _max = max(feed, key=lambda x: x[self.key])[self.key]
        return list(filter(lambda x: x[self.key] >= _max * self.cutoff, feed))


class TopN:

    def __init__(self, n):
        self.n = n

    def __call__(self, feed):
        return feed[:self.n]


def do_select(selector, feed):
    if selector is not None:
        return selector(feed)
    else:
        return feed
