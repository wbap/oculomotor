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

        self.retina = Component(retina, interval=1, offset=0, sleep=0)
        self.lip = Component(lip, interval=1, offset=1, sleep=0) 
        self.it = Component(it, interval=1, offset=1, sleep=0)
        self.ad = Component(ad, interval=1, offset=2, sleep=0)
        self.fef = Component(fef, interval=1, offset=3, sleep=0)

        self.fef(self.ad(self.lip(self.retina), self.it(self.retina)))

        self.scheduler = Scheduler(self.retina, self.lip, self.it, self.ad, self.fef)

    def __call__(self, obs, reward, done):
        self.retina.in_ports[0].send(obs)
        self.scheduler.next()
        action = self.fef.out_port.recv()
        
        if action is None:
            return np.array([0.0, 0.0], dtype=np.float32)
        return action
