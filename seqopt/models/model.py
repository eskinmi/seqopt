import seqopt


class OptModel:
    """
    :type: seqopt.models.model.OptModel

    The model that optimizes the given initial
    sequence based on the feedback. There are
    two (2) important submodules the model inputs:
        - seqopt.optimizers.optimizers
            Manages the optimization with its given
                configurations / strategy.
        - seqopt.callbacks
            Callbacks

    Args:
        input_sequence: input seq to optimize (list[dict])
        optimizer: optimizer object (seqopt.optimizers.optimizer.OptStrategy)
        population: population keys list (list[str])
        episodes: number of episodes (int)
        opt_interval: episodes intervals for optimization (int)
        progress: progress callback (seqopt.callbacks.Progress)
        max_items: max items output seq can have (int)

    """
    def __init__(self,
                 input_sequence,
                 optimizer,
                 population=None,
                 episodes=None,
                 opt_interval=1,
                 progress=None,
                 max_items=None
                 ):
        self.input = input_sequence
        self.episodes = episodes
        self.episode = 0
        self.interval = opt_interval
        self.optimizer = optimizer
        self.stopper = seqopt.callbacks.EpisodeLimit(n_episodes=self.episodes)
        self.logger = seqopt.callbacks.Logs(population)

        if max_items is not None:
            self.max_items = max_items
        else:
            self.max_items = len(self.input)

        if not progress:
            self.progress = seqopt.callbacks.Progress(patience=None, start_at=0)
        else:
            self.progress = progress

    @property
    def is_opt_episode(self):
        return False if bool(self.episode % self.interval) else True

    def opt(self, feed):
        """
        Optimize the sequence with number of input
            given overtime.
        :param feed: feedback (list)
        :param optimize: optimize in round.
        :return:
            optimized sequence (list)
        """
        self.stopper.invoke(self.logger.logs)
        if self.stopper.stop or self.progress.stop:
            return self.logger.feed_opt
        self.logger.log_feed(feed)
        if self.is_opt_episode:
            feed_opt = self.optimizer(self.logger)[:self.max_items]
        else:
            if self.logger.logs:
                feed_opt = self.logger.feed_opt
            else:
                feed_opt = self.logger.feed[:self.max_items]
        self.logger.log_episode({'episode': self.episode, 'feed': feed, 'feed_opt': feed_opt})
        self.progress.invoke(self.logger.logs)
        self.episode += 1
        return feed_opt
