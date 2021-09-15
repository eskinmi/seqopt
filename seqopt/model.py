from seqopt import process
from seqopt import callbacks
from seqopt.optimizers import scorers
from seqopt.optimizers import selectors
import pickle


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
        scorer: (scorers.ScoringStrategy)
        selector: (selectors)
        n_try: number of items to try per opt (int)
        add_to: add index strategy (str)
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
                 early_stop_patience=None,
                 early_stop_start_at=0,
                 reset_experiment=False
                 ):
        super().__init__(population=population)
        self.interval = opt_interval
        self.selector = selector
        self.scorer = scorer
        self.trials = process.Trials(n=n_try, add_to=add_to)
        self.progress = callbacks.Progress(n_episodes=episodes,
                                           patience=early_stop_patience,
                                           start_at=early_stop_start_at,
                                           restart=reset_experiment)

    @property
    def _is_opt_episode(self):
        """
        Finds if the current episode is
        optimization episode.
        :return:
            bool
        """
        return False if bool(self.episode % self.interval) else True

    def _add_trial_items(self):
        self.items_to_try, self.feed_out = self.trials.run(self.feed_out, self.unused_items)

    def _run_opt_episode(self, feed):
        self.log_feed(feed)
        if self._is_opt_episode:
            self.feed_out = selectors.do_select(
                self.selector, scorers.do_score(self.scorer, self.feeds))
            self._add_trial_items()
        self.log_episode(self.episode, self._is_opt_episode)
        self.episode += 1

    def opt(self, feed):
        self.progress.invoke(self.logs, self.unused_items, self.initial_population)
        if self.progress.restart:
            self.reset_experiment()
            self.progress.reset()
            self._run_opt_episode(feed)
        elif self.progress.stop:
            self.reset_experiment()
        else:
            self._run_opt_episode(feed)


def load(path):
    """
    Load process.
    :param path: path (str)
    :return:
        seqopt.model
    """
    with open(path, 'r') as f:
        model = pickle.load(f)
    return model


def save(model, path):
    """
    Checkpoint the process on a given episode.
    :param model: seqopt.model
    :param path: checkpoint location (str)
    """
    with open(f'{path}/seqopt', 'w') as f:
        pickle.dump(model, f)




