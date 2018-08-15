# -*- coding: utf-8 -*-
import brica
import os
import cv2
import math
import numpy as np

GRID_DIVISION = 8
GRID_WIDTH = 128 // GRID_DIVISION

ACCUMULAATE_DECAY_RATE = 0.98
CURSOR_MATCH_COEFF = 0.1


class Accumulator(object):
    def __init__(self, ex, ey):
        """
        Arguments:
          ex: Float eye move dir x
          ey: Float eye move dir Y
        """
        # Accumulated likehilood
        self.likelihood = 0.0
        self.ex = ex
        self.ey = ey
        
    def accumulate(self, value):
        self.likelihood += value
        self.likelihood = np.clip(self.likelihood, 0.0, 1.0)
        
        # Decay likelihood
        self.likelihood *= ACCUMULAATE_DECAY_RATE

    def reset(self):
        self.likelihood = 0.0

    @property
    def output(self):
        return [self.likelihood, self.ex, self.ey]


class SaliencyAccumulator(Accumulator):
    def __init__(self, pixel_x, pixel_y, ex, ey):
        super(SaliencyAccumulator, self).__init__(ex, ey)
        # Pixel x,y pos at left top corner of the region.
        self.pixel_x = pixel_x
        self.pixel_y = pixel_y
        
    def process(self, saliency_map):
        pass


class CursorAccumulator(Accumulator):
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
        match = cv2.matchTemplate(region_image, self.cursor_template, cv2.TM_CCOEFF_NORMED)
        # Find the maximum match value
        match_rate = np.max(match)
        self.accumulate(match_rate * CURSOR_MATCH_COEFF)
        
        
class FEF(object):
    def __init__(self):
        self.timing = brica.Timing(4, 1, 0)
        
        self.saliency_accumulators = []
        self.cursor_accumulators = []
        
        cursor_template = self._load_image("data/debug_cursor_template_w.png")
        
        for i in range(GRID_DIVISION):
            pixel_x = GRID_WIDTH * i
            cx = 2.0 / GRID_DIVISION * (i + 0.5) - 1.0
            
            for j in range(GRID_DIVISION):
                pixel_y = GRID_WIDTH * j
                cy = 2.0 / GRID_DIVISION * (j + 0.5) - 1.0
                
                ex = cx
                ey = -cy

                #saliency_accumulator = SaliencyAccumulator(pixel_x, pixel_y, ex, ey)
                #self.saliency_accumulators.append(saliency_accumulator)
                
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
        
        saliency_map = inputs['from_lip']
        retina_image = inputs['from_vc']
        
        #for saliency_accumulator in self.saliency_accumulators:
        #    saliency_accumulator.process(saliency_map)
        for cursor_accumulator in self.cursor_accumulators:
            cursor_accumulator.process(retina_image)
        
        output = self._collect_output()
        
        return dict(to_pfc=None,
                    to_bg=output,
                    to_sc=output)

    def _collect_output(self):
        output = []
        # TODO: saliency accumulatorの対応まだ
        for cursor_accumulator in self.cursor_accumulators:
            output.append(cursor_accumulator.output)
        return output

    def _load_image(self, file_path):
        module_dir, _ = os.path.split(os.path.realpath(__file__))
        absolute_path = os.path.join(module_dir, file_path)
        image = cv2.imread(absolute_path)
        return image
