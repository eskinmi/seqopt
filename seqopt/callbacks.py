class Progress:
    """
    Progress monitors the progress of the
    experiments and stops the process when necessary.


    """

    def __init__(self,
                 early_stop_start_at=0,
                 early_stop_patience=2
                 ):
        self.patience = early_stop_patience
        self.start_at = early_stop_start_at
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
                    self.is_stagnant = True
                    print('process will be stopped.')
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




