import numpy as np

class FEF(object):
    def __init__(self):
        pass

    def __call__(self, x):
        dx = np.random.uniform(low=-0.02, high=0.02)
        dy = np.random.uniform(low=-0.02, high=0.02)
        return np.array([dx, dy])
