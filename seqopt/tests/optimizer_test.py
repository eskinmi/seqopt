from seqopt.optimizers.helpers import *


def test_feed_repositionn_pos():
    _feed = [
        {'key': 'A', 'reward': 98, 'pos': 0},
        {'key': 'B', 'reward': 80, 'pos': 0},
        {'key': 'C', 'reward': 20, 'pos': 0},
        {'key': 'D', 'reward': 58, 'pos': 0},
        {'key': 'E', 'reward': 69, 'pos': 0}
    ]
    _out = feed_reposition(_feed)
    assert sorted([f['pos'] for f in _out]) == list(range(0,5))
