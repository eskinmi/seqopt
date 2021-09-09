# seqopt

This package helps solve naive sequence optimization problems,
that includes sorting and selecting a population of keys with their
relative rewards (the feedback).

The input to the model (feed) should be a list of dictionaries,
containing `key` = name, `reward` = feedback (scalar), `pos` : position (optional).

## usage
===

an example usage with a log normalization :

```py

from seqopt import model
progress = model.callbacks.Progress(patience=2, do_stop=True)
scorer = model.scorers.LogNorm(per_episode=False)
selector = model.selectors.MaxRelative(cutoff_ratio=0.90)
seq_opt = model.SeqOpt(scorer=scorer,
                       selector=selector,
                       progress=progress,
                       episodes=20,
                       n_try=1,
                       add_to='last',
                       opt_interval=2,
                       reset_experiment=True,
                       population=population
                       ))

tour=0
while tour < len(input_feeds):
  seq_opt.opt(input_feeds[tour])
  tour+=1


```



