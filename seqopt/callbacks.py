class EpisodeLimit:

    def __init__(self,
                 n_episodes,
                 ):
        self.episodes = n_episodes
        self.stop = False

    def reset(self):
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
        self.last_keys = []

    def reset(self):
        self.stop = False
        self.is_stagnant = False
        self.n = 0
        self.last_keys = []

    def invoke(self, logs):
        if logs and self.patience is not None and logs[-1]['is_opt_episode']:
            episode, episode_num = logs[-1], logs[-1]['episode']
            cur_keys = [row.get('key') for row in episode['feed_out']]
            if self.start_at <= episode_num and self.last_keys == cur_keys:
                self.n += 1
                if self.n >= self.patience:
                    print('reached the optimized state. Process can be ended.')
                    self.is_stagnant = True
                    if self.do_stop:
                        print('process will be stopped.')
                        self.stop = True
                else:
                    self.last_keys = cur_keys
            else:
                self.n = 0
                self.last_keys = cur_keys


