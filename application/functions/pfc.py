import cv2
import numpy as np

import brica
from .utils import load_image

"""
This is a sample implemention of PFC (Prefrontal cortex) module.
You can change this as you like.
"""

class Phase(object):
    INIT = -1  # Initial phase
    START = 0  # Start phase while finding red cross cursor
    TARGET = 1 # Target finding phsae


class CursorFindAccumulator(object):
    def __init__(self, decay_rate=0.9):
        # Accumulated likelilood
        self.decay_rate = decay_rate
        self.likelihood = 0.0
        
        self.cursor_template = load_image("data/debug_cursor_template_w.png")
        
    def accumulate(self, value):
        self.likelihood += value
        self.likelihood = np.clip(self.likelihood, 0.0, 1.0)
        
    def reset(self):
        self.likelihood = 0.0

    def process(self, retina_image):
        match = cv2.matchTemplate(retina_image, self.cursor_template,
                                  cv2.TM_CCOEFF_NORMED)
        match_rate = np.max(match)
        self.accumulate(match_rate * 0.1)

    def post_process(self):
        # Decay likelihood
        self.likelihood *= self.decay_rate



class PFC(object):
    def __init__(self):
        self.timing = brica.Timing(3, 1, 0)
        
        self.cursor_find_accmulator = CursorFindAccumulator()
        
        self.phase = Phase.INIT

        
    def __call__(self, inputs):
        if 'from_vc' not in inputs:
            raise Exception('PFC did not recieve from VC')
        if 'from_fef' not in inputs:
            raise Exception('PFC did not recieve from FEF')
        if 'from_bg' not in inputs:
            raise Exception('PFC did not recieve from BG')
        if 'from_hp' not in inputs:
            raise Exception('PFC did not recieve from HP')

        # Image from Visual cortex module.
        retina_image = inputs['from_vc']
        # Allocentrix map image from hippocampal formatin module.
        map_image = inputs['from_hp']

        # This is a very sample implementation of phase detection.
        # You should change here as you like.
        self.cursor_find_accmulator.process(retina_image)
        self.cursor_find_accmulator.post_process()
        
        if self.phase == Phase.INIT:
            if self.cursor_find_accmulator.likelihood > 0.7:
                self.phase = Phase.START
        elif self.phase == Phase.START:
            if self.cursor_find_accmulator.likelihood < 0.4:
                self.phase = Phase.TARGET
        else:
            if self.cursor_find_accmulator.likelihood > 0.6:
                self.phase = Phase.START
        
        if self.phase == Phase.INIT or self.phase == Phase.START:
            # TODO: 領野をまたいだ共通phaseをどう定義するか？
            fef_message = 0
        else:
            fef_message = 1

        return dict(to_fef=fef_message,
                    to_bg=None)
