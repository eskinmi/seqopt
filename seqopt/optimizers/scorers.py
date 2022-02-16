import seqopt.optimizers.helpers
import numpy
from abc import ABC, abstractmethod


class Scorers(ABC):
    """
    Scoring main class with aggregation strategies, and main score functions call.
        :param per_episode: score per episode (bool)
        :param agg_strategy: aggregation func (str)
    """
    def __init__(self,
                 per_episode=True,
                 agg_strategy='mean',
                 ):
        self.per_episode = per_episode
        self.agg_strategy = agg_strategy
        self.agg_method = getattr(numpy, self.agg_strategy)
        self.m_key = 'score'

    @property
    def agg_strategy(self):
        return self._agg_strategy

    @agg_strategy.setter
    def agg_strategy(self, value):
        acceptable = ['mean', 'sum', 'min', 'max']
        if value not in acceptable:
            raise ValueError(f'agg_strategy can only be : {acceptable}')
        else:
            self._agg_strategy = value

    def agg(self, feeds):
        """
        Aggregate all logged feeds based on given
            aggregation strategy.
        :param feeds: seqopt.Logs.feeds (list)
        :return:
            aggregated feeds (list)
        """
        if not self.per_episode:
            units_dict = {}
            [
                units_dict.update({i['key']: units_dict.get(i['key'], []) + [i['reward']]})
                for feed in feeds for i in feed
             ]
            units_dict_agg = {k: self.agg_method(v) for k,v in units_dict.items()}
            agg_list = [{'key': k, 'pos': 0, 'reward': v} for k, v in units_dict_agg.items()]
            return seqopt.optimizers.helpers.reposition(agg_list, 'reward')
        else:
            return seqopt.optimizers.helpers.reposition(feeds[-1], 'reward')

    @abstractmethod
    def score(self, feed):
        pass

    def apply(self, feeds):
        return seqopt.optimizers.helpers.reposition(self.score(self.agg(feeds)))


class Naive(Scorers):
    """
    Naive scorer.
        score = reward.
    :return:
        list[dict] with new key (score).
    """
    def __init__(self,
                 per_episode=True,
                 agg_strategy='sum'
                 ):
        super().__init__(per_episode, agg_strategy)

    def score(self, feed):
        return seqopt.optimizers.helpers.feed_naive(feed, self.m_key)


class Share(Scorers):
    """
    Naive scorer.
        score = reward.
    :return:
        list[dict] with new key (score).
    """
    def __init__(self,
                 per_episode=True,
                 agg_strategy='sum'
                 ):
        super().__init__(per_episode, agg_strategy)

    def score(self, feed):
        return seqopt.optimizers.helpers.feed_share(feed, self.m_key)


class MinMaxNorm(Scorers):
    """
        Min Max Normalizer.
        score = min_max_norm(feed).
        :return:
            list[dict] with new key (score).
        """
    def __init__(self,
                 per_episode=True,
                 agg_strategy='sum'
                 ):
        super().__init__(per_episode, agg_strategy)

    def score(self, feed):
        return seqopt.optimizers.helpers.feed_min_max_norm(feed, self.m_key)


class LogNorm(Scorers):
    """
        Log normalizer.
        score = log_norm(feed)
            :param log_base: log base (int/float)
        :return:
            list[dict] with new key (score).
        """
    def __init__(self,
                 log_base=10,
                 per_episode=True,
                 agg_strategy='sum'
                 ):
        self.log_base = log_base if log_base is not None else seqopt.optimizers.helpers.math.e
        super().__init__(per_episode, agg_strategy)

    def score(self, feed):
        return seqopt.optimizers.helpers.feed_log_norm(feed, self.log_base, self.m_key)


class StandardNorm(Scorers):
    """
        Standard normalizer.
        score = standard_norm(feed).
        :return:
            list[dict] with new key (score).
        """
    def __init__(self,
                 per_episode=True,
                 agg_strategy='sum'
                 ):
        super().__init__(per_episode, agg_strategy)

    def score(self, feed):
        return seqopt.optimizers.helpers.feed_standard_score(feed, self.m_key)


_default_scorer = Naive(per_episode=True)


def apply(scorer, feeds):
    if scorer is not None:
        return scorer.apply(feeds)
    else:
        return _default_scorer.apply(feeds)
