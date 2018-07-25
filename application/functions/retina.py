# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import math
import cv2



class Retina(object):
    """ Retina module.
    
    Inputs original environment image and output image with blurrly gray-scaled
    peripheral vision effect.
    """
    
    def __init__(self):
        # Size of the buffer. (Should be changed along with environment setting)
        buffer_width = 128
        # Calculate mixing rate
        self.mix_rates, self.inv_mix_rates = self.create_mix_rates(buffer_width)

    def __call__(self, x):
        # Create retina image with blurrly gray-scaled peripheral vision effect.
        retina_img = self.create_retina_image(x, self.mix_rates, self.inv_mix_rates)
        return retina_img

    def create_retina_image(self, img, rates, inv_rates):
        # First create blurred and gray-scaled image
        blur_img = self.create_blur_image(img)
        # Then mix orignal image and blurred image using mixing rates
        retina_img = img * rates + blur_img * inv_rates
        return retina_img.astype(np.uint8)

    def create_mix_rates(self, width):
        """ Caluclate mixing rate for original and blurred, gray-scaled image """
        
        radius = width / 2 * 0.65
    
        rates = [0.0] * (width * width)
        hw = width // 2
        for i in range(width):
            x = i - hw
            for j in range(width):
                y = j - hw
                r = math.sqrt(x*x + y*y)
                rate = r / radius
                #rate = rate * rate
                if rate > 1.0:
                    rate = 1.0
                rate = (1.0 - rate) * 1.5
                if rate > 1.0:
                    rate = 1.0
                rates[j*width + i] = rate
        rates = np.array(rates)
        rates = rates.reshape([width, width, 1])
        inv_rates = 1.0 - rates
        return rates, inv_rates

    def create_blur_image(self, img):
        """ Create blurred image from original image. """
        
        h = img.shape[0]
        w = img.shape[1]

        # Create blurred image. First shurink orignal image.

        # Resizeing to 1/2 size
        resized_img0 = cv2.resize(img,
                                  dsize=(h//2, w//2),
                                  interpolation=cv2.INTER_LINEAR)
        # Resizeing to 1/4 size
        resized_img1 = cv2.resize(resized_img0,
                                  dsize=(h//4, w//4),
                                  interpolation=cv2.INTER_LINEAR)
        # Resizeing to 1/8 size
        resized_img2 = cv2.resize(resized_img1,
                                  dsize=(h//8, w//8),
                                  interpolation=cv2.INTER_LINEAR)

        # After that, magnify shrinked image to original size
        blur_img = cv2.resize(resized_img2,
                              dsize=(h, w),
                              interpolation=cv2.INTER_LINEAR)

        # Convert blurred image into gray-scaled image
        gray_blur_img = cv2.cvtColor(blur_img, cv2.COLOR_BGR2GRAY)
        gray_blur_img = np.reshape(gray_blur_img,
                                   [gray_blur_img.shape[0], gray_blur_img.shape[0], 1])
        gray_blur_img = np.tile(gray_blur_img, 3)
        return gray_blur_img
