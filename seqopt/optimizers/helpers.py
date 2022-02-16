import numpy
import math


def reposition(feed, by_key='reward'):
    f_repos = []
    for pos, d in enumerate(sorted(feed, key=lambda x: x[by_key], reverse=True)):
        d_ = d.copy()
        d_['pos'] = pos
        f_repos.append(d_)
    return f_repos


def reposition_by_index(feed):
    f_repos = []
    for pos, d in enumerate(feed):
        d_ = d.copy()
        d_['pos'] = pos
        f_repos.append(d_)
    return f_repos


def feed_naive(feed, name):
    metrics = []
    for d in feed:
        d_ = d.copy()
        d_[name] = d['reward']
        metrics.append(d_)
    return metrics


def feed_min_max_norm(feed, name):
    metrics = []
    max_ = max(feed, key=lambda x: x['reward'])['reward']
    min_ = min(feed, key=lambda x: x['reward'])['reward']
    for i in feed:
        i[name] = round((i['reward'] - min_) / (max_ - min_), 5)
        metrics.append(i)
    return metrics


def feed_share(feed, name):
    metrics = []
    sum_ = sum([i['reward'] for i in feed])
    for i in feed:
        i[name] = i['reward'] / sum_
        metrics.append(i)
    return metrics


def feed_log_norm(feed, log_base, name):
    metrics = []
    for i in feed:
        i[name] = round(math.log(i['reward']+1, log_base), 5)
        metrics.append(i)
    return metrics


def feed_standard_score(feeds, name):
    metrics = []
    avg_ = numpy.mean([i['reward'] for i in feeds])
    std_ = numpy.std([i['reward'] for i in feeds])
    for i in feeds:
        i[name] = round((i['reward'] - avg_) / std_, 5)
        metrics.append(i)
    return metrics
