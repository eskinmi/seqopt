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

from seqopt import OptModel
from seqopt import callbacks
from seqopt import optimizers

model = OptModel(
  input_sequence=input_seq,
  population=population,
  optimizer=optimizers.strategy.LogNormOpt(per_episode=False, agg_strategy='sum', log_base=None, cutoff_point=0.20),
  progress=callbacks.Progress(patience=2, do_stop=True),
  max_items=3,
  episodes=None,  
  opt_interval=1
)

i = 0
while not stop:
  feed_opt = model.opt(FEEDS[i])
  stop = model.progress.stop
  i+=1
  if i == len(FEEDS)-1:
    break


```



