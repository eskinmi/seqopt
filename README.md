# seqopt

This package helps solve naive sequence optimization problems,
that includes sorting and selecting, trying a population of keys with their
relative rewards (the feedback).
This model can be used for recursive optimization problems where the output is the  
input to a system for the new iteration, from which the new rewards are collected.


## terminology

`Experiment` : An experiment is a complete trial cycle, where all the keys in the  
population is tried and feedback is collected. Experiments are looged at the end  
of the experiments in `seqopt.model.experiments`. Experiment logs are collected in
`seqopt.model.logger` object.


## example use

The input to the model (feed) should be a list of dictionaries,
containing `key` = name, `reward` = feedback (scalar), `pos` : position (optional).
An example usage with a min max normalization :

```py

from seqopt import model
scr = model.scorers.MinMaxNorm(per_episode=False, agg_strategy='mean')
sel = model.selectors.MaxRelative(cutoff_ratio=0.75)

seq_opt = model.SeqOpt(scorer=scr,
                       selector=sel,
                       episodes=20,
                       n_try=2,
                       add_to='last',
                       opt_interval=2,
                       reset_experiment=False,
                       early_stop_patience=2,
                       population=population
                       )

for feed in input_feeds:
  seq_opt.opt(feed)
  
print(f'optimized version : {seq_opt.optimized_seq}')
print(f'experiments : {seq_opt.experiments}')
print('current experiment logs : {seq_opt.logger.logs}')
```

## modules
### scorers
`seqopt.scorer` module manages the scoring schema of feed from a given
experiment, with out of box such as `LogNorm`, `MinMaxNorm`, or `StandardNorm`.

The `ScoringStrategy` object allows users to use make their own scorers.  
In order to write a custom scorer, one can use the following approach:

```py
class CustomScorer(ScoringStrategy):

    def __init__(self,
                 per_episode=True,
                 agg_strategy='sum'
                 ):
        super().__init__(per_episode, agg_strategy)

    def score(self, feed):
        #scoring operation
        return feed_scored
```

### selectors
selectors manage the selecting schema for every optimization round. Currrently,
the package has two out of box selectors, `TopN` and `MaxRelative`.




