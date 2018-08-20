# -*- coding: utf-8 -*-
import os
import cv2
import math
import numpy as np

import brica
from .utils import load_image

GRID_DIVISION = 8
GRID_WIDTH = 128 // GRID_DIVISION

CURSOR_MATCH_COEFF = 0.1
SALIENCY_COEFF = 0.3


class ActionAccumulator(object):
    def __init__(self, ex, ey, decay_rate=0.9):
        """
        Arguments:
          ex: Float eye move dir x
          ey: Float eye move dir Y
        """
        # Accumulated likehilood
        self.likelihood = 0.0
        self.ex = ex
        self.ey = ey
        self.decay_rate = decay_rate
        
    def accumulate(self, value):
        self.likelihood += value
        self.likelihood = np.clip(self.likelihood, 0.0, 1.0)

    def post_process(self):
        # Decay likelihood
        self.likelihood *= self.decay_rate

    def reset(self):
        self.likelihood = 0.0

    @property
    def output(self):
        return [self.likelihood, self.ex, self.ey]


class SaliencyAccumulator(ActionAccumulator):
    def __init__(self, pixel_x, pixel_y, ex, ey):
        super(SaliencyAccumulator, self).__init__(ex, ey, decay_rate=0.85)
        # Pixel x,y pos at left top corner of the region.
        self.pixel_x = pixel_x
        self.pixel_y = pixel_y
        
    def process(self, saliency_map):
        # Crop region image
        region_saliency = saliency_map[self.pixel_y:self.pixel_y+GRID_WIDTH,
                                       self.pixel_x:self.pixel_x+GRID_WIDTH]
        average_saliency = np.mean(region_saliency)
        self.accumulate(average_saliency * CURSOR_MATCH_COEFF)
        

class CursorAccumulator(ActionAccumulator):
    def __init__(self, pixel_x, pixel_y, ex, ey, cursor_template):
        super(CursorAccumulator, self).__init__(ex, ey)
        # Pixel x,y pos at left top corner of the region.
        self.pixel_x = pixel_x
        self.pixel_y = pixel_y
        self.cursor_template = cursor_template
        
    def process(self, retina_image):
        # Crop region image
        region_image = retina_image[self.pixel_y:self.pixel_y+GRID_WIDTH,
                                    self.pixel_x:self.pixel_x+GRID_WIDTH, :]
        # Calculate template matching
        match = cv2.matchTemplate(region_image, self.cursor_template,
                                  cv2.TM_CCOEFF_NORMED)
        # Find the maximum match value
        match_rate = np.max(match)
        self.accumulate(match_rate * SALIENCY_COEFF)
        

class FEF(object):
    def __init__(self):
        self.timing = brica.Timing(4, 1, 0)
        
        self.saliency_accumulators = []
        self.cursor_accumulators = []
        
        cursor_template = load_image("data/debug_cursor_template_w.png")
        
        for ix in range(GRID_DIVISION):
            pixel_x = GRID_WIDTH * ix
            cx = 2.0 / GRID_DIVISION * (ix + 0.5) - 1.0
            
            for iy in range(GRID_DIVISION):
                pixel_y = GRID_WIDTH * iy
                cy = 2.0 / GRID_DIVISION * (iy + 0.5) - 1.0
                
                ex = -cx
                ey = -cy
                
                saliency_accumulator = SaliencyAccumulator(pixel_x, pixel_y, ex, ey)
                self.saliency_accumulators.append(saliency_accumulator)
                
                cursor_accumulator = CursorAccumulator(pixel_x, pixel_y, ex, ey,
                                                       cursor_template)
                self.cursor_accumulators.append(cursor_accumulator)
                
    def __call__(self, inputs):
        if 'from_lip' not in inputs:
            raise Exception('FEF did not recieve from LIP')
        if 'from_vc' not in inputs:
            raise Exception('FEF did not recieve from VC')
        if 'from_pfc' not in inputs:
            raise Exception('FEF did not recieve from PFC')
        if 'from_bg' not in inputs:
            raise Exception('FEF did not recieve from BG')

        phase = inputs['from_pfc']

        saliency_map, optical_flow = inputs['from_lip']
        retina_image = inputs['from_vc']
        
        # TODO: 領野をまたいだ共通phaseをどう定義するか？
        if phase == 0:
            for cursor_accumulator in self.cursor_accumulators:
                cursor_accumulator.process(retina_image)
        else:
            for saliency_accumulator in self.saliency_accumulators:
                saliency_accumulator.process(saliency_map)

        for saliency_accumulator in self.saliency_accumulators:
            saliency_accumulator.post_process()
        for cursor_accumulator in self.cursor_accumulators:
            cursor_accumulator.post_process()
        
        output = self._collect_output()
        
        #self._debug_analysis()
        
        return dict(to_pfc=None,
                    to_bg=output,
                    to_sc=output)

    def _collect_output(self):
        output = []
        for saliency_accumulator in self.saliency_accumulators:
            output.append(saliency_accumulator.output)
        for cursor_accumulator in self.cursor_accumulators:
            output.append(cursor_accumulator.output)            
        return output

    def _debug_analysis(self):
        cursor_likelihoods = []
        for cursor_accumulator in self.cursor_accumulators:
            cursor_likelihoods.append(cursor_accumulator.likelihood)
            
        saliency_likelihoods = []
        for saliency_accumulator in self.saliency_accumulators:
            saliency_likelihoods.append(saliency_accumulator.likelihood)
