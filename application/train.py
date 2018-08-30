# -*- coding: utf-8 -*-
"""
 Training script for oculomotor tasks.
"""

import argparse

from agent import Agent
from functions import BG, FEF, LIP, PFC, Retina, SC, VC, HP, CB
from oculoenv import Environment
from oculoenv import PointToTargetContent, ChangeDetectionContent, OddOneOutContent, VisualSearchContent, \
    MultipleObjectTrackingContent, RandomDotMotionDiscriminationContent
from logger import Logger



class Contents(object):
    POINT_TO_TARGET = 1
    CHANGE_DETECTION = 2
    ODD_ONE_OUT = 3
    VISUAL_SEARCH = 4
    MULTIPLE_OBJECT_TRACKING = 5
    RANDOM_DOT_MOTION_DISCRIMINATION = 6


def get_content(content_type):
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


def train(content, step_size, logger):
    retina = Retina()
    lip = LIP()
    vc = VC()
    pfc = PFC()
    fef = FEF()
    bg = BG()
    sc = SC()
    hp = HP()
    cb = CB()
    
    agent = Agent(
        retina=retina,
        lip=lip,
        vc=vc,
        pfc=pfc,
        fef=fef,
        bg=bg,
        sc=sc,
        hp=hp,
        cb=cb
    )
    
    env = Environment(content)

    # If your training code is written inside BG module, please add model load code here like.
    #
    #   bg.load_model("model.pkl")
    #
    # When runnning with Docker, directory under 'oculomotor/' is volume shared
    # with the host, so you can load/save the model data at anywhere under 'oculomotor/' dir.
    
    obs = env.reset()
    
    reward = 0
    done = False
    
    episode_reward = 0
    episode_count = 0

    # Add initial reward log
    logger.log("episode_reward", episode_reward, episode_count)
    
    for i in range(step_size):
        image, angle = obs['screen'], obs['angle']
        # Choose action by the agent's decision
        action = agent(image, angle, reward, done)
        # Foward environment one step
        obs, reward, done, _ = env.step(action)
        
        episode_reward += reward

        if done:
            obs = env.reset()
            print("episode reward={}".format(episode_reward))

            # Store log for tensorboard graph
            episode_count += 1
            logger.log("episode_reward", episode_reward, episode_count)
            
            episode_reward = 0
            
            # Plase add model save code as you like.
            #
            # if i % 10 == 0:
            #     bg.save_model("model.pkl")
            
    print("training finished")
    logger.close()
    


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
    parser.add_argument("--step_size", help="Training step size", type=int, default=1000000)
    parser.add_argument("--log_file", help="Log file name", type=str, default="experiment0")
    
    args = parser.parse_args()
    
    content_type = args.content
    step_size = args.step_size
    log_file = args.log_file

    # Create task content
    content = get_content(content_type)
    
    print("start training content: {} step_size={}".format(content_type, step_size))

    # Log is stored 'log' directory
    log_path = "log/{}".format(log_file)
    logger = Logger(log_path)

    # Start training
    train(content, step_size, logger)


if __name__ == '__main__':
    main()
