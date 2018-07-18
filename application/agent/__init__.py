from pybrica import Component, Scheduler
import numpy as np


class ActionDelegate(object):
    def __init__(self, working_memory, pattern_matcher, state_manager):
        self.working_memory = working_memory
        self.pattern_matcher = pattern_matcher
        self.state_manager = state_manager

    def __call__(self, lip, it):
        return lip


class Agent(object):
    def __init__(self, retina, lip, it, working_memory, pattern_matcher, state_manager, fef):
        ad = ActionDelegate(working_memory, pattern_matcher, state_manager)

        self.retina = Component(retina, interval=1, offset=0, sleep=3)
        self.lip = Component(lip, interval=1, offset=1, sleep=3) 
        self.it = Component(it, interval=1, offset=1, sleep=3)
        self.ad = Component(ad, interval=1, offset=2, sleep=3)
        self.fef = Component(fef, interval=1, offset=3, sleep=3)

        self.fef(self.ad(self.lip(self.retina), self.it(self.retina)))

        self.scheduler = Scheduler(self.retina, self.lip, self.it, self.ad, self.fef)

    def __call__(self, obs, reward, done):
        dx = np.random.uniform(low=-0.02, high=0.02)
        dy = np.random.uniform(low=-0.02, high=0.02)
        return np.array([dx, dy])
