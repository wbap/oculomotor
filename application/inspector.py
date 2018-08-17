# Debug inspector

import numpy as np
import pygame, sys
from pygame.locals import *

from agent import Agent
from functions import BG, FEF, LIP, PFC, Retina, SC, VC
from oculoenv import PointToTargetContent, Environment


BLUE    = (128, 128, 255)
RED     = (255, 192, 192)
BLACK   = (0, 0, 0)
WHITE   = (255, 255, 255)

DARK_GRAY = (64, 64, 64)


class Display(object):
    def __init__(self, display_size):
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

        self.agent = Agent(retina=self.retina,
                           lip=self.lip,
                           vc=self.vc,
                           pfc=self.pfc,
                           fef=self.fef,
                           bg=self.bg,
                           sc=self.sc)

        content = PointToTargetContent(target_size="small",
                                       use_lure=True,
                                       lure_size="large")
        self.env = Environment(content)
        obs = self.env.reset()
        
        self.last_image = obs['screen']
        self.last_angle = obs['angle']
        self.last_reward = 0
        self.last_done = False
        
        self.episode_reward = 0
        
        self.font = pygame.font.Font(None, 20)
        
    def update(self):
        self.surface.fill(BLACK)
        self.process()
        pygame.display.update()
        
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
        self.show_image(data, 128+8, 8, "retina")
        
    def show_saliency_map(self, saliency_map):
        saliency_map_ = np.clip(saliency_map * 255.0, 0.0, 255.0)
        data = saliency_map_.astype(np.uint8)
        data = np.stack([data for _ in range(3)], axis=2)
        self.show_image(data, 128*2+8, 8, "saliency")
        
    def show_image(self, data, left, top, label):
        image = pygame.image.frombuffer(data, (128,128), 'RGB')
        self.surface.blit(image, (left, top))
        self.draw_center_text(label, 128/2 + left, top + 128 + 8)
        
    def show_reward(self):
        self.draw_text("REWARD: {}".format(int(self.episode_reward)), 128 * 3 + 8 + 8, 10)
        
    def show_fef_data(self, fef_data):
        fef_data_len = len(fef_data)

        bottom = 256 + 16
        pygame.draw.line(self.surface, DARK_GRAY,
                         (8, bottom-100),
                         (3*fef_data_len+8, bottom-100), 1)
        
        for i,data in enumerate(fef_data):
            likelihood = data[0]
            left = 8 + 3 * i
            top = bottom - 100 * likelihood
            pygame.draw.line(self.surface, WHITE, (left,  top), (left,  bottom), 1)
        
        self.draw_center_text("likelihoods", (8+3*fef_data_len)//2, bottom + 8)
        
    def process(self):
        action = self.agent(self.last_image,
                            self.last_angle,
                            self.last_reward,
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
            
        if self.sc.last_fef_data is not None:
            self.show_fef_data(self.sc.last_fef_data)
            
        self.last_image = image
        self.last_angle = angle
        self.last_reward = reward
        self.last_done = done
        

def main():
    FPS = 60
    
    display_size = (500, 400)
    display = Display(display_size)
    
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
