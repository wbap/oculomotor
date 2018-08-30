# -*- coding: utf-8 -*-
"""
Debug local inspector tool without web interface.
"""

import numpy as np
import argparse
import pygame, sys
from pygame.locals import *
import cv2

from oculoenv import PointToTargetContent, ChangeDetectionContent, OddOneOutContent, \
    VisualSearchContent, MultipleObjectTrackingContent, RandomDotMotionDiscriminationContent
from inspector import Inspector


RECORDING = False

CONTENT_POINT_TO_TARGET = 1
CONTENT_CHANGE_DETECTION = 2
CONTENT_ODD_ONE_OUT = 3
CONTENT_VISUAL_SEARCH = 4
CONTENT_MULTIPLE_OBJECT_TRACKING = 5
CONTENT_RANDOM_DOT_MOTION_DISCRIMINATION = 6


class MovieWriter(object):
  def __init__(self, file_name, frame_size, fps):
    """
    frame_size is (w, h)
    """
    self._frame_size = frame_size
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    self.vout = cv2.VideoWriter()
    success = self.vout.open(file_name, fourcc, fps, frame_size, True)
    if not success:
        print("Create movie failed: {0}".format(file_name))

  def add_frame(self, frame):
    """
    frame shape is (h, w, 3), dtype is np.uint8
    """
    self.vout.write(frame)

  def close(self):
      self.vout.release() 
      self.vout = None


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
    args = parser.parse_args()
    
    content_type = args.content
    
    if content_type == CONTENT_POINT_TO_TARGET:
        content = PointToTargetContent()
    elif content_type == CONTENT_CHANGE_DETECTION:
        content = ChangeDetectionContent()
    elif content_type == CONTENT_ODD_ONE_OUT:
        content = OddOneOutContent()
    elif content_type == CONTENT_VISUAL_SEARCH:
        content = VisualSearchContent()
    elif content_type == CONTENT_MULTIPLE_OBJECT_TRACKING:
        content = MultipleObjectTrackingContent()
    else:
        content = RandomDotMotionDiscriminationContent()

    FPS = 60
    display_size = (128*4+16, 500)
    inspector = Inspector(content, display_size)
    
    clock = pygame.time.Clock()
    running = True

    frame_count = 0

    if RECORDING:
        writer = MovieWriter("out.mov", inspector.display_size, FPS)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        inspector.update()
        clock.tick(FPS)

        if RECORDING:
            d = inspector.get_frame()
            writer.add_frame(d)

            frame_count += 1

            if frame_count > 1000:
                running = False

    if RECORDING:
        writer.close()

if __name__ == '__main__':
    main()
