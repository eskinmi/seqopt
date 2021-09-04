import seqopt.optimizers.helpers
from seqopt.callbacks import Logs
import numpy


class OptStrategy:

    def __init__(self,
                 per_episode=True,
                 agg_strategy='sum',
                 ):
        self.per_episode = per_episode
        self._acc_strategy = ['mean', 'sum', 'min', 'max']
        if agg_strategy not in self._acc_strategy:
            raise ValueError(f'agg_strategy must be one of these values : {self._acc_strategy}')
        self.agg_strategy = agg_strategy
        self.agg_method = getattr(numpy, self.agg_strategy)

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
            return seqopt.optimizers.helpers.feed_reposition(agg_list, 'reward')
        else:
            return seqopt.optimizers.helpers.feed_reposition(feeds[-1], 'reward')


class NaiveOpt(OptStrategy):

    def __init__(self,
                 cutoff_point=0.25,
                 per_episode=True,
                 agg_strategy='sum'
                 ):
        self.cutoff_point = cutoff_point
        super().__init__(per_episode, agg_strategy)
        self.m_key = f'{agg_strategy}_score'

    def __call__(self, logger: Logs):
        feed_agg = super().agg(logger.feeds)
        feed_mtr = seqopt.optimizers.helpers.feed_naive(feed_agg, self.m_key)
        feed_opt = list(filter(lambda x: x[self.m_key] >= 1 * self.cutoff_point, feed_mtr))
        return seqopt.optimizers.helpers.feed_reposition(feed_opt, self.m_key)


class MinMaxScaleOpt(OptStrategy):

    def __init__(self,
                 cutoff_point=0.25,
                 per_episode=True,
                 agg_strategy='sum'
                 ):
        self.cutoff_point = cutoff_point
        super().__init__(per_episode, agg_strategy)
        self.m_key = 'min_max_norm_score'

    def __call__(self, logger: Logs):
        feed_agg = super().agg(logger.feeds)
        feed_mtr = seqopt.optimizers.helpers.feed_min_max_norm(feed_agg, self.m_key)
        feed_opt = list(filter(lambda x: x[self.m_key] >= 1 * self.cutoff_point, feed_mtr))
        return seqopt.optimizers.helpers.feed_reposition(feed_opt, self.m_key)


class LogNormOpt(OptStrategy):

    def __init__(self,
                 log_base=10,
                 cutoff_point=0.25,
                 per_episode=True,
                 agg_strategy='sum'
                 ):
        self.log_base = log_base if log_base is not None else seqopt.optimizers.helpers.math.e
        self.cutoff_point = cutoff_point
        super().__init__(per_episode, agg_strategy)
        self.m_key = 'log_norm_score'

    def __call__(self, logger: Logs):
        feed_agg = super().agg(logger.feeds)
        feed_mtr = seqopt.optimizers.helpers.feed_log_norm(feed_agg, self.log_base, self.m_key)
        feed_opt = list(filter(lambda x: x[self.m_key] >= 1 * self.cutoff_point, feed_mtr))
        return seqopt.optimizers.helpers.feed_reposition(feed_opt, self.m_key)


class StandardScoreOpt(OptStrategy):

    def __init__(self,
                 ucl=3.0,
                 lcl=3.0,
                 per_episode=True,
                 agg_strategy='sum'
                 ):
        if ucl < 0 or lcl < 0:
            raise ValueError('upper and lower confidence limits should be positive integer.')
        self.ucl = ucl
        self.lcl = -1 * lcl
        super().__init__(per_episode, agg_strategy)
        self.m_key = 'standard_score'

    def __call__(self, logger: Logs):
        feed_agg = super().agg(logger.feeds)
        feed_mtr = seqopt.optimizers.helpers.feed_standard_score(feed_agg, self.m_key)
        feed_opt = list(filter(lambda x: x[self.m_key] >= self.lcl and x[self.m_key] >= self.lcl, feed_mtr))
        return seqopt.optimizers.helpers.feed_reposition(feed_opt, self.m_key)


# class EpsilonGreedyBandit(OptStrategy):
#
#     def __init__(self,
#                  epsilon=None,
#                  per_episode=False,
#                  agg_strategy='sum'
#                  ):
#         super().__init__(per_episode, agg_strategy)
#         self.epsilon = epsilon
#         self.m_key = 'epsilon_greedy_bandit_score'

