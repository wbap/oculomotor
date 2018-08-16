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

"""
debug_image_index = 0
def debug_save_image(image):
    from skimage import io

    global debug_image_index
    image = np.flip(image, 0) # Flip image upside down
    file_name = "out_{0:04d}.png".format(debug_image_index)
    io.imsave(file_name, image)
    debug_image_index += 1
"""

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

        image = obs['screen']
        #debug_save_image(image)


if __name__ == '__main__':
    main()
