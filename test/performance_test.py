# -*- coding: utf-8 -*-
import unittest
import time

import numpy as np

from agent import Agent
from functions import BG, FEF, LIP, PFC, Retina, SC, VC, HP, CB
from oculoenv import Environment
from oculoenv import PointToTargetContent, ChangeDetectionContent, OddOneOutContent, VisualSearchContent, \
    MultipleObjectTrackingContent, RandomDotMotionDiscriminationContent

class Contents(object):
    POINT_TO_TARGET = 1
    CHANGE_DETECTION = 2
    ODD_ONE_OUT = 3
    VISUAL_SEARCH = 4
    MULTIPLE_OBJECT_TRACKING = 5
    RANDOM_DOT_MOTION_DISCRIMINATION = 6


class TestPerformance(unittest.TestCase):
    def get_content(self, content_type):
        if content_type == Contents.POINT_TO_TARGET:
            content = PointToTargetContent()
        elif content_type == Contents.CHANGE_DETECTION:
            content = ChangeDetectionContent()
        elif content_type == Contents.ODD_ONE_OUT:
            content = OddOneOutContent()
        elif content_type == Contents.VISUAL_SEARCH:
            content = VisualSearchContent()
        elif content_type == Contents.MULTIPLE_OBJECT_TRACKING:
            content = MultipleObjectTrackingContent()
        else:
            content = RandomDotMotionDiscriminationContent()
        return content

    def calc_fps(self, content_type, with_agent):
        content = self.get_content(content_type)

        if with_agent:
            agent = Agent(
                retina=Retina(),
                lip=LIP(),
                vc=VC(),
                pfc=PFC(),
                fef=FEF(),
                bg=BG(),
                sc=SC(),
                hp=HP(),
                cb=CB()
            )
    
        env = Environment(content)
        obs = env.reset()

        reward = 0
        done = False
        
        step_size = 1000
        
        step = 0

        start = time.time()
        
        for i in range(step_size):
            if with_agent:
                image, angle = obs['screen'], obs['angle']
                dummy_action = agent(image, angle, reward, done)
            
            dh = np.random.uniform(low=-0.05, high=0.05)
            dv = np.random.uniform(low=-0.05, high=0.05)
            action = np.array([dh, dv])
            
            obs, reward, done, _ = env.step(action)
            step += 1
            if done:
                obs = env.reset()

        elapsed_time = time.time() - start
        fps = step_size / elapsed_time
        return fps


    def test_agent_performance(self):
        print("check performance with agent")
        for i in range(1, 7):
            fps = self.calc_fps(i, with_agent=True)
            print("  content={0} fps={1:.2f}".format(i, fps))

    def test_environment_performance(self):
        print("check performance without agent")
        for i in range(1, 7):
            fps = self.calc_fps(i, with_agent=False)
            print("  content={0} fps={1:.2f}".format(i, fps))



if __name__ == '__main__':
    unittest.main()
