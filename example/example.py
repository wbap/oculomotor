# -*- coding: utf-8 -*-
import sys
import argparse

import pyglet
import numpy as np

import gym
from agi_lab import PointToTargetContent, Environment


def save_numpy_img(file_name, img):
  img = np.ascontiguousarray(img)
  img = np.flip(img, 0)

  from skimage import io
  io.imsave(file_name, img)

lastImgNo = 0

def save_img(img):
  global lastImgNo
  save_numpy_img('out_%03d.png' % lastImgNo, img)
  lastImgNo += 1


def check_offscreen():
  content = PointToTargetContent()
  env = Environment(content)

  start = time.time()

  frame_size = 1000

  for i in range(frame_size):
    obs = env.render_offscreen()

  elapsed_time = time.time() - start
  fps = 1.0 / (elapsed_time / frame_size)

  print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")
  print ("fps:{0}".format(fps))

  save_img(obs)




import pyglet

content = PointToTargetContent()
env = Environment(content)
env.render() # env.window is created here

# 1フレーム目が画面が出ないバグがある

@env.window.event
def on_key_press(symbol, modifiers):
  from pyglet.window import key

  action = None
  if symbol == key.LEFT:
    print('left')
    action = np.array([0.00, 1.00])
  elif symbol == key.RIGHT:
    print('right')
    action = np.array([0.00, -1.00])
  elif symbol == key.UP:
    print('up')
    action = np.array([1.00, 0.00])
  elif symbol == key.DOWN:
    print('down')
    action = np.array([-1.00, 0.00])
  elif symbol == key.BACKSPACE or symbol == key.SLASH:
    print('RESET')
    action = None
    env.reset()
    env.render()
  elif symbol == key.ESCAPE:
    env.close()
    sys.exit(0)
  else:
    return

  if action is not None:
    obs, reward, done, info = env.step(action)
    print('reward=%d' % (reward))
    env.render()

    if done:
      print('done!')
      env.reset()
      env.render()


pyglet.app.run()

env.close()



