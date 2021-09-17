# seqopt

This package helps solve naive sequence optimization problems,
that includes sorting and selecting, trying a population of keys with their
relative rewards (the feedback).
This model can be used for recursive optimization problems where the output is the  
input to a system for the new iteration, from which the new rewards are collected.


## terminology

`Experiment` : An experiment is a complete trial cycle, where all the keys in the  
population is tried and feedback is collected. Experiments are logged in property  
`seqopt.model.experiments`. Each experiment is logged in `seqopt.model.experiment_logs`  
during the course of the experiment.


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
                       episodes=None,
                       n_try=1,
                       add_to='last',
                       opt_interval=2,
                       reset_experiment=True,
                       early_stop_patience=2,
                       population=population
                       )
                       
for feed in input_feeds:
  seq_opt.opt(feed)
  
seq_opt.experiments
```

## optimizers
### scorers
`seqopt.scorer` module manages the scoring schema of feed from a given
experiment, with out of box such as `LogNorm`, `MinMaxNorm`, or `StandardNorm`.
Scorer.score function accepts a feed argument, which is either the last feed,
or aggregation of all feeds in the experiment (based on per_episode arg).
The `Scorers` object allows users to use make their own scorers.  
In order to write a custom scorer, one can use the following approach:


```py
from seqopt import optimizers
class CustomScorer(optimizers.scorers.Scorer):

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
Selectors manage the selecting method for every optimization round. Currently,
the package has three out of box selectors, `TopN`, `MaxRelative` and
`AbsoluteThreshold`. Similar to scorers, any selection method can be given to the model , which has a call  
method that inputs the output of the scorer (latest feed or  aggregated feeds). The `Selector` object  
allows users to make their own selector.


```py
from seqopt import optimizers
class CustomSelector(optimizers.selectors.Selector):

    def __init__(self, a, b):
        super().__init__()
        self.a = a
        self.b = b

    def select(self, feed):
        #selecting operation
        return selected_feed.
        
```



