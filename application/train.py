# -*- coding: utf-8 -*-
import argparse

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


def get_content(content_type):
    if content_type == Contents.POINT_TO_TARGET:
        content = PointToTargetContent(target_size="small",
                                       use_lure=True,
                                       lure_size="large")
    elif content_type == Contents.CHANGE_DETECTION:
        content = ChangeDetectionContent(target_number=3,
                                         max_learning_count=20,
                                         max_interval_count=10)
    elif content_type == Contents.ODD_ONE_OUT:
        content = OddOneOutContent()
    elif content_type == Contents.VISUAL_SEARCH:
        content = VisualSearchContent()
    elif content_type == Contents.MULTIPLE_OBJECT_TRACKING:
        content = MultipleObjectTrackingContent()
    else:
        content = RandomDotMotionDiscriminationContent()
    return content


def train(content, step_size):
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
    
    episode_reward = 0

    step = 0
    
    for i in range(step_size):
        image, angle = obs['screen'], obs['angle']
        
        action = agent(image, angle, reward, done)
        obs, reward, done, _ = env.step(action)

        episode_reward += reward
        step += 1

        if done:
            obs = env.reset()
            print("episode reward={}".format(episode_reward))
            episode_reward = 0
            
            
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--content",
                        help="1: Point To Target"
                        + " 2: Change Detection"
                        + " 3: Odd One Out"
                        + " 4: Visual Search"
                        + " 5: Multiple Object Tracking"
                        + " 6: Random Dot Motion Descrimination",
                        type=int,
                        default=1)
    parser.add_argument("--step_size", help="Training step size", type=int, default=10000)
    
    args = parser.parse_args()
    
    content_type = args.content
    step_size = args.step_size
    
    content = get_content(content_type)
    
    print("start training content: {} step_size={}".format(content_type, step_size))
    
    train(content, step_size)
    
    
if __name__ == '__main__':
    main()
