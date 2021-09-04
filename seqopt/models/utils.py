import pickle


def load_model(path):
    """
    Load models.
    :param path:
    :return:
    """
    with open(path, 'r') as f:
        model = pickle.load(f)
    return model


def save_model(model, path):
    """
    Checkpoint the models on a given episode.
    :param model: seqopt models.
    :param path: checkpoint location (str)
    """
    with open(f'{path}/models', 'w') as f:
        pickle.dump(model, f)

