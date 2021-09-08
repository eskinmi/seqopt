from seqopt.process import process
from seqopt import callbacks
from seqopt.optimizers import scorers
from seqopt.optimizers import selectors


class SeqOpt(process.Experiments):
    """
    :type: seqopt.process.model.OptModel

    The model that optimizes the given initial
    sequence based on the feedback. There are
    two (2) important submodules the model inputs:
        - seqopt.optimizers.optimizers
            Manages the optimization with its given
                configurations / strategy.
        - seqopt.callbacks
            Callbacks

        opt func excepts a feed that is a list of
            dictionary that hosts the feedback for
            keys in following schema:
                [
                    'key' : name (str),
                    'reward'  : reward (int / float)
                    'pos' : position (int) (optional)
                ]

    Args:
        trials: (process.ItemTrials)
        scorer: (scorers.ScoringStrategy)
        selector: (selectors)
        population: population keys list (list[str])
        episodes: number of episodes (int)
        opt_interval: episodes intervals for optimization (int)
        progress: progress callback (seqopt.callbacks.Progress)
        reset_experiment: reset at the end of trial (bool) (default, False)
    """
    def __init__(self,
                 scorer=None,
                 selector=None,
                 n_try=0,
                 add_to='last',
                 population=None,
                 episodes=None,
                 opt_interval=1,
                 progress=None,
                 reset_experiment=False
                 ):
        super().__init__(logger=process.Logs(population),
                         reset_at_end=reset_experiment)
        self.interval = opt_interval
        self.stopper = callbacks.EpisodeLimit(n_episodes=episodes)
        self.selector = selector
        self.scorer = scorer
        self.trials = process.ItemTrials(n=n_try, add_to=add_to)

        if not progress:
            self.progress = callbacks.Progress(patience=None, start_at=0)
        else:
            self.progress = progress

    @property
    def is_opt_episode(self):
        return False if bool(self.episode % self.interval) else True

    def select_and_score(self):
        self.logger.feed_out = selectors.do_select(self.selector,
                                                   scorers.do_score(self.scorer,
                                                                    self.logger))

    def add_new(self):
        self.logger.items_to_try, self.logger.feed_out = process.do_trial(self.trials, self.logger)

    def opt(self, feed):
        """
        Optimize the sequence with number of input
            given overtime.
        :param feed: feedback (list)
        :return:
            optimized sequence (list)
        """
        self.stopper.invoke(self.logger.logs)
        if self.stopper.stop or self.progress.stop:
            return self.logger.logs[-1]
        self.logger.log_feed(feed)
        if self.is_opt_episode:
            self.select_and_score()
            self.add_new()
            self.logger.log_episode(self.episode, self.is_opt_episode)
            self.progress.invoke(self.logger.logs)
        if self.reset:
            self.log_and_reset()
        else:
            self.episode += 1
        return self.logger.logs[-1]
