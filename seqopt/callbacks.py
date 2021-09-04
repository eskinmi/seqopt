from collections import Counter


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
        self.last_episode = {'feed_opt': None}

    def invoke(self, logs):
        if logs and self.patience is not None:
            episode_log = logs[-1]
            episode_num = episode_log['episode']
            if self.start_at <= episode_num and self.last_episode['feed_opt'] == episode_log['feed_opt']:
                if self.n < self.patience:
                    self.n += 1
                    self.last_episode = episode_log
                else:
                    if self.verbose:
                        print('reached the optimized state. Process can be ended.')
                    self.is_stagnant = True
                    if self.do_stop:
                        print('process will be stopped.')
                        self.stop = True
            else:
                self.n = 0
                self.last_episode = episode_log


class Logs:

    def __init__(self, population=None):
        self.initial_population = population
        self.population = self.initial_population
        self.feeds = []
        self.logs = []
        self.counter = Counter()
        self.feed = None
        self.feed_opt = None

    def log_feed(self, feed):
        self.feeds.append(feed)
        self.feed = feed
        self.counter.update([i['key'] for i in feed])
        if self.initial_population is None:
            self.population = list(self.counter.keys())

    def log_episode(self, log):
        self.logs.append(log)
        self.feed_opt = self.logs[-1]['feed_opt']