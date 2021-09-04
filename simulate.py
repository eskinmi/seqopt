from string import ascii_uppercase
import random

SET_LENGTH = 5

input_seq = [
    dict(key=ascii_uppercase[pos], pos=pos)
    for pos in range(SET_LENGTH)
]


def generate_random_rewards(input_sequence, minimum=0, maximum=100):
    """
    Generate random reward for the set feed.
    :param input_sequence: feed (list)
    :param minimum: min reward (int)
    :param maximum: max reward (int
    :return:
        feed (list(dict))
    """
    feed_reward = []
    for ss in input_sequence:
        ss['reward'] = random.randint(minimum+1, maximum+1)
        feed_reward.append(ss)
    return feed_reward


FEEDS = [
    [
        {'key': 'A', 'reward': 98, 'pos': 0},
        {'key': 'B', 'reward': 80, 'pos': 1},
        {'key': 'C', 'reward': 20, 'pos': 2},
        {'key': 'D', 'reward': 58, 'pos': 3},
        {'key': 'E', 'reward': 69, 'pos': 4}
    ],
    [
        {'key': 'A', 'reward': 51, 'pos': 0},
        {'key': 'B', 'reward': 91, 'pos': 1},
        {'key': 'C', 'reward': 92, 'pos': 2},
        {'key': 'D', 'reward': 28, 'pos': 3},
        {'key': 'E', 'reward': 76, 'pos': 4}
    ],
    [
        {'key': 'A', 'reward': 99, 'pos': 0},
        {'key': 'B', 'reward': 74, 'pos': 1},
        {'key': 'C', 'reward': 60, 'pos': 2},
        {'key': 'D', 'reward': 96, 'pos': 3},
        {'key': 'E', 'reward': 68, 'pos': 4}
    ],
    [
        {'key': 'A', 'pos': 0, 'reward': 39},
        {'key': 'B', 'pos': 1, 'reward': 41},
        {'key': 'C', 'pos': 2, 'reward': 42},
        {'key': 'D', 'pos': 3, 'reward': 50},
        {'key': 'E', 'pos': 4, 'reward': 93}
    ],
[
        {'key': 'A', 'pos': 0, 'reward': 39},
        {'key': 'B', 'pos': 1, 'reward': 41},
        {'key': 'C', 'pos': 2, 'reward': 42},
        {'key': 'D', 'pos': 3, 'reward': 50},
        {'key': 'E', 'pos': 4, 'reward': 93}
    ],
[
        {'key': 'A', 'pos': 0, 'reward': 39},
        {'key': 'B', 'pos': 1, 'reward': 41},
        {'key': 'C', 'pos': 2, 'reward': 42},
        {'key': 'D', 'pos': 3, 'reward': 50},
        {'key': 'E', 'pos': 4, 'reward': 93}
    ],
[
        {'key': 'A', 'pos': 0, 'reward': 39},
        {'key': 'B', 'pos': 1, 'reward': 41},
        {'key': 'C', 'pos': 2, 'reward': 42},
        {'key': 'D', 'pos': 3, 'reward': 50},
        {'key': 'E', 'pos': 4, 'reward': 93}
    ],
[
        {'key': 'A', 'pos': 0, 'reward': 39},
        {'key': 'B', 'pos': 1, 'reward': 41},
        {'key': 'C', 'pos': 2, 'reward': 42},
        {'key': 'D', 'pos': 3, 'reward': 50},
        {'key': 'E', 'pos': 4, 'reward': 93}
    ],

]

# from seqopt import OptModel
# from seqopt import callbacks
# from seqopt import optimizers
# import simulate
# model = OptModel(
#     input_sequence=simulate.input_seq,
#     max_items=3,
#     episodes=10,
#     optimizer=optimizers.MinMaxScaleOpt(per_episode=True, agg_strategy='sum'),
#     progress=callbacks.Progress(patience=2, do_stop=True)
#     )
# OPT_PER_ROUND = 3
# feed_opt = model.compile(simulate.FEEDS[0])
