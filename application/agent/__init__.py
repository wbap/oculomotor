import numpy as np


class Agent(object):
    def __init__(self):
        pass

    def __call__(self, obs, reward, done):
        action = None
        if action is None:
            return np.array([0.0, 0.0], dtype=np.float32)
        return action
