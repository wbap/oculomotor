from pybrica import Component, Scheduler
import numpy as np


class Agent(object):
    def __init__(self):
        pass

    def __call__(self, obs, reward, done):
        self.retina.in_ports[0].send(obs)
        self.scheduler.next()
        action = self.fef.out_port.recv()
        
        if action is None:
            return np.array([0.0, 0.0], dtype=np.float32)
        return action
