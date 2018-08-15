# Stand alone application for debugging

import numpy as np

from agent import Agent

from functions import BG, FEF, LIP, PFC, Retina, SC, VC

from oculoenv import PointToTargetContent, Environment

SHOW_DISPLAY = True


agent = Agent(retina=Retina(),
              lip=LIP(),
              vc=VC(),
              pfc=PFC(),
              fef=FEF(),
              bg=BG(),
              sc=SC())

def main():
    content = PointToTargetContent(
        target_size="small", use_lure=True, lure_size="large")    
    env = Environment(content)
    
    if SHOW_DISPLAY:
        env.render()

    frame_size = 1000

    reward = 0
    done = False

    obs = env.reset()

    for i in range(frame_size):
        image = obs['screen']
        angle = obs['angle']
        
        action = agent(image, angle, reward, done)
        obs, reward, done, _ = env.step(action)
        
        if SHOW_DISPLAY:
            env.render()
            
        print("reward = {}".format(reward))
        
        if done:
            print("Episode terminated")
            obs = env.reset()


if __name__ == '__main__':
    main()
