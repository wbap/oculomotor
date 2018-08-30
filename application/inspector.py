# -*- coding: utf-8 -*-
"""
Visualize processed processed image, state, etc in each function component of the Agent.
This inspector renders these information into an image, and it can be retrieved by get_frame().
"""

import math
import time

import numpy as np
import cv2
import pygame, sys
from pygame.locals import *

from agent import Agent
from functions import BG, FEF, LIP, PFC, Retina, SC, VC, HP, CB
from oculoenv import Environment

from oculoenv import PointToTargetContent, ChangeDetectionContent, OddOneOutContent, VisualSearchContent, MultipleObjectTrackingContent, RandomDotMotionDiscriminationContent

BLUE = (128, 128, 255)
RED = (255, 192, 192)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

DARK_GRAY = (64, 64, 64)


class Inspector(object):
    def __init__(self, content, display_size):
        pygame.init()

        self.surface = pygame.display.set_mode(display_size, 0, 24)
        pygame.display.set_caption('oculomotor')

        self.retina = Retina()
        self.lip = LIP()
        self.vc = VC()
        self.pfc = PFC()
        self.fef = FEF()
        self.bg = BG()
        self.sc = SC()
        self.hp = HP()
        self.cb = CB()

        self.agent = Agent(
            retina=self.retina,
            lip=self.lip,
            vc=self.vc,
            pfc=self.pfc,
            fef=self.fef,
            bg=self.bg,
            sc=self.sc,
            hp=self.hp,
            cb=self.cb
        )

        self.env = Environment(content)
        obs = self.env.reset()

        self.last_image = obs['screen']
        self.last_angle = obs['angle']
        self.last_reward = 0
        self.last_done = False

        self.episode_reward = 0

        self.font = pygame.font.Font(None, 20)

        self.display_size = display_size

    def update(self):
        self.surface.fill(BLACK)
        done = self.process()
        pygame.display.update()
        return done

    def draw_text(self, str, left, top, color=WHITE):
        text = self.font.render(str, True, color, BLACK)
        text_rect = text.get_rect()
        text_rect.left = left
        text_rect.top = top
        self.surface.blit(text, text_rect)

    def draw_center_text(self, str, center_x, top):
        text = self.font.render(str, True, WHITE, BLACK)
        text_rect = text.get_rect()
        text_rect.centerx = center_x
        text_rect.top = top
        self.surface.blit(text, text_rect)

    def show_original_image(self, image):
        image_ = image * 1.0
        data = image_.astype(np.uint8)
        self.show_image(data, 8, 8, "input")

    def show_retina_image(self, image):
        image_ = image * 1.0
        data = image_.astype(np.uint8)
        self.show_image(data, 128 + 8, 8, "retina")

    def show_saliency_map(self, saliency_map):
        saliency_map_ = np.clip(saliency_map * 255.0, 0.0, 255.0)
        data = saliency_map_.astype(np.uint8)
        data = np.stack([data for _ in range(3)], axis=2)
        self.show_image(data, 128 * 2 + 8, 8, "saliency")

    def show_optical_flow(self, optical_flow):
        # Show optical flow with HSV color image
        image = self.get_optical_flow_hsv(optical_flow)

        # Draw optical flow direction with lines
        step = 16

        h, w = optical_flow.shape[:2]
        y, x = np.mgrid[step // 2:h:step, step // 2:w:step].reshape(
            2, -1).astype(int)
        fx, fy = optical_flow[y, x].T
        lines = np.vstack([x, y, x + fx, y + fy]).T.reshape(-1, 2, 2)
        lines = np.int32(lines + 0.5)

        cv2.polylines(image, lines, 0, (0, 255, 0))
        for (x1, y1), (x2, y2) in lines:
            cv2.circle(image, (x1, y1), 1, (0, 255, 0), -1)
        self.show_image(image, 128 * 3 + 8, 8, "opt_flow")

    def show_map_image(self, map_image):
        # Show allocentric map image in the Hippocampal formation.
        self.show_image(map_image, 128 * 3 + 8, 300, "allocentric map")

    def get_optical_flow_hsv(self, optical_flow):
        h, w = optical_flow.shape[:2]
        fx, fy = optical_flow[:, :, 0], optical_flow[:, :, 1]
        ang = np.arctan2(fy, fx) + np.pi
        v = np.sqrt(fx * fx + fy * fy)
        hsv = np.zeros((h, w, 3), np.uint8)
        hsv[..., 0] = ang * (180 / np.pi / 2)
        hsv[..., 1] = 255
        hsv[..., 2] = np.minimum(v * 4, 255)
        image = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
        return image

    def show_image(self, data, left, top, label):
        image = pygame.image.frombuffer(data, (128, 128), 'RGB')
        self.surface.blit(image, (left, top))
        self.draw_center_text(label, 128 / 2 + left, top + 128 + 8)
        pygame.draw.rect(self.surface, DARK_GRAY, Rect(left, top, 128, 128), 1)

    def show_reward(self):
        self.draw_text("REWARD: {}".format(int(self.episode_reward)),
                       128 * 3 + 24, 128 + 48)

    def show_fef_data_bars(self, fef_data):
        fef_data_len = len(fef_data)

        bottom = 256 + 16
        pygame.draw.line(self.surface, DARK_GRAY, (8, bottom - 100),
                         (3 * fef_data_len + 8, bottom - 100), 1)

        for i, data in enumerate(fef_data):
            likelihood = data[0]
            left = 8 + 3 * i
            top = bottom - 100 * likelihood
            pygame.draw.line(self.surface, WHITE, (left, top), (left, bottom),
                             1)

        self.draw_center_text("likelihoods", (8 + 3 * fef_data_len) // 2,
                              bottom + 8)

    def show_fef_data_grid(self, fef_data):
        grid_division = int(math.sqrt(len(fef_data) // 2))
        grid_width = 128 // grid_division

        likelihoods0 = []
        likelihoods1 = []

        data_len = len(fef_data) // 2

        for i in range(data_len):
            likelihoods0.append(fef_data[i][0])
            likelihoods1.append(fef_data[i + data_len][0])

        self.show_grid(likelihoods0, 0, grid_division, grid_width, 8, 300,
                       "saliency acc")
        self.show_grid(likelihoods1, 0, grid_division, grid_width, 8 + 128,
                       300, "cursor acc")

    def show_grid(self, data, offset, grid_division, grid_width, left, top,
                  label):
        index = 0
        for ix in range(grid_division):
            x = grid_width * ix
            for iy in range(grid_division):
                y = grid_width * iy
                likelihood = data[index]
                c = int(likelihood * 255.0)
                color = (c, c, c)
                pygame.draw.rect(self.surface, color,
                                 Rect(left + x, top + y, grid_width,
                                      grid_width))
                index += 1
        pygame.draw.rect(self.surface, DARK_GRAY, Rect(left, top, 128, 128), 1)
        self.draw_center_text(label, 128 / 2 + left, top + 128 + 8)

    def process(self):
        action = self.agent(self.last_image, self.last_angle, self.last_reward,
                            self.last_done)
        obs, reward, done, _ = self.env.step(action)

        self.episode_reward += reward

        if done:
            obs = self.env.reset()
            self.episode_reward = 0

        image = obs['screen']
        angle = obs['angle']

        self.show_reward()

        self.show_original_image(image)

        if self.retina.last_retina_image is not None:
            self.show_retina_image(self.retina.last_retina_image)

        if self.lip.last_saliency_map is not None:
            self.show_saliency_map(self.lip.last_saliency_map)

        if self.lip.last_optical_flow is not None:
            self.show_optical_flow(self.lip.last_optical_flow)

        if self.sc.last_fef_data is not None:
            self.show_fef_data_bars(self.sc.last_fef_data)
            self.show_fef_data_grid(self.sc.last_fef_data)

        if self.hp.map_image is not None:
            self.show_map_image(self.hp.map_image)

        self.last_image = image
        self.last_angle = angle
        self.last_reward = reward
        self.last_done = done

        return done

    def get_frame(self):
        data = self.surface.get_buffer().raw
        image = np.fromstring(data, dtype=np.uint8)
        image = image.reshape((self.display_size[1], self.display_size[0], 3))
        return image
