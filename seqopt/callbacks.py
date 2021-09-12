class Progress:
    """
    Progress monitors the progress of the
    experiments and stops the process when necessary.
    There are two stop options for the program.
        - episode limit
            Episode limit stops the experiments when max episode is
            reached.
        - early stop
            Early stop is activated when parameter early_stop_patience
            is given. If set to None, the experiments wont stop when it is
            stagnant.

        :param patience: number of episodes to wait, before early stop(int)
        :param start_at: the episode to start checking early stop from (int)
        ;param n_episodes: number of episodes (int)
    """

    def __init__(self,
                 n_episodes=None,
                 patience=None,
                 start_at=0
                 ):
        self.episodes = n_episodes
        self.patience = patience
        self.start_at = start_at
        self.stop = False
        self.is_stagnant = False
        self.n = 0
        self.last_keys = []

    def reset(self):
        self.stop = False
        self.is_stagnant = False
        self.n = 0
        self.last_keys = []

    def early_stop(self, logs):
        if logs and self.patience is not None and logs[-1]['is_opt_episode']:
            episode, episode_num = logs[-1], logs[-1]['episode']
            cur_keys = [row.get('key') for row in episode['feed_out']]
            if self.start_at <= episode_num and self.last_keys == cur_keys:
                self.n += 1
                if self.n >= self.patience:
                    print('reached the optimized state, process can be ended.')
                    print('process will be stopped.')
                    self.is_stagnant = True
                    self.stop = True
                else:
                    self.last_keys = cur_keys
            else:
                self.n = 0
                self.last_keys = cur_keys

    def episode_stopper(self, logs):
        if self.episodes is not None and logs:
            if logs[-1]['episode'] >= self.episodes-1:
                print('reached end of episodes for this experiment')
                self.stop = True

    def invoke(self, logs):
        self.episode_stopper(logs)
        self.early_stop(logs)




