class EpisodeLimit:

    def __init__(self,
                 n_episodes,
                 ):
        self.episodes = n_episodes
        self.stop = False

    def invoke(self, logs):
        if self.episodes is not None and logs:
            if logs[-1]['episode'] >= self.episodes-1:
                self.stop = True


class Progress:

    def __init__(self,
                 patience=2,
                 start_at=0,
                 verbose=True,
                 do_stop=False
                 ):
        self.patience = patience
        self.start_at = start_at
        self.verbose = verbose
        self.do_stop = do_stop
        self.stop = False
        self.is_stagnant = False
        self.n = 0
        self.last_episode_keys = []

    def invoke(self, logs):
        if logs and self.patience is not None:
            episode_log = logs[-1]
            episode_keys = [row.get('key') for row in episode_log['feed_out']]
            episode_num = episode_log['episode']
            if self.start_at <= episode_num and self.last_episode_keys == episode_keys:
                if self.n < self.patience:
                    self.n += 1
                    self.last_episode_keys = episode_keys
                else:
                    if self.verbose:
                        print('reached the optimized state. Process can be ended.')
                    self.is_stagnant = True
                    if self.do_stop:
                        print('process will be stopped.')
                        self.stop = True
            else:
                self.n = 0
                self.last_episode_keys = episode_keys
        return None


