import seqopt.optimizers.helpers
import numpy


class ScoringStrategy:

    def __init__(self,
                 per_episode=True,
                 agg_strategy='mean',
                 ):
        self.per_episode = per_episode
        self._acc_strategy = ['mean', 'sum', 'min', 'max']
        if agg_strategy not in self._acc_strategy:
            raise ValueError(f'agg_strategy must be one of these values : {self._acc_strategy}')
        self.agg_strategy = agg_strategy
        self.agg_method = getattr(numpy, self.agg_strategy)
        self.m_key='score'

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

    def __call__(self, logger):
        return seqopt.optimizers.helpers.reposition(
            self.score(
                self.agg(logger.feeds)))


class Naive(ScoringStrategy):

    def __init__(self,
                 per_episode=True,
                 agg_strategy='sum'
                 ):
        super().__init__(per_episode, agg_strategy)

    def score(self, feed):
        return seqopt.optimizers.helpers.feed_naive(feed, self.m_key)


class MinMaxNorm(ScoringStrategy):

    def __init__(self,
                 per_episode=True,
                 agg_strategy='sum'
                 ):
        super().__init__(per_episode, agg_strategy)

    def score(self, feed):
        return seqopt.optimizers.helpers.feed_min_max_norm(feed, self.m_key)


class LogNorm(ScoringStrategy):

    def __init__(self,
                 log_base=10,
                 per_episode=True,
                 agg_strategy='sum'
                 ):
        self.log_base = log_base if log_base is not None else seqopt.optimizers.helpers.math.e
        super().__init__(per_episode, agg_strategy)

    def score(self, feed):
        return seqopt.optimizers.helpers.feed_log_norm(feed, self.log_base, self.m_key)


class StandardNorm(ScoringStrategy):

    def __init__(self,
                 per_episode=True,
                 agg_strategy='sum'
                 ):
        super().__init__(per_episode, agg_strategy)

    def score(self, feed):
        return seqopt.optimizers.helpers.feed_standard_score(feed, self.m_key)


_default_scorer = Naive(per_episode=True)


def do_score(scorer, logger):
    if scorer is not None:
        return scorer(logger)
    else:
        return _default_scorer(logger)
