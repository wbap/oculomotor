import cv2
import math
import numpy as np

import brica

class Retina(object):
    """ Retina module.

    This retina module takes environemnt image and outputs processed image with 
    peripheral vision.
    
    Peripheral pixels are blurred and gray-scaled.
    """
    
    def __init__(self):
        self.timing = brica.Timing(1, 1, 0)
        
        width = 128
        self.rates, self.inv_rates = self._create_rate_datas(width)

        self.last_retina_image = None

    def __call__(self, inputs):
        if 'from_environment' not in inputs:
            raise Exception('Retina did not recieve from Retina')
        
        image, angle = inputs['from_environment']
        retina_image = self._create_retina_image(image)

        # Store retina image for debug visualizer
        self.last_retina_image = retina_image

        return dict(to_lip=retina_image,
                    to_vc=retina_image,
                    to_hp=(retina_image, angle))

    def _create_rate_datas(self, width):
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

    def _create_blur_image(self, image):
        h = image.shape[0]
        w = image.shape[1]

        # Resizeing to 1/2 size
        resized_image0 = cv2.resize(image,
                                  dsize=(h//2, w//2),
                                  interpolation=cv2.INTER_LINEAR)
        # Resizeing to 1/4 size
        resized_image1 = cv2.resize(resized_image0,
                                  dsize=(h//4, w//4),
                                  interpolation=cv2.INTER_LINEAR)
        # Resizeing to 1/8 size
        resized_image2 = cv2.resize(resized_image1,
                                  dsize=(h//8, w//8),
                                  interpolation=cv2.INTER_LINEAR)
        
        # Resizing to original size
        blur_image = cv2.resize(resized_image2,
                              dsize=(h, w),
                              interpolation=cv2.INTER_LINEAR)

        # Conver to Grayscale
        gray_blur_image = cv2.cvtColor(blur_image, cv2.COLOR_BGR2GRAY)
        gray_blur_image = np.reshape(gray_blur_image,
                                     [gray_blur_image.shape[0],
                                      gray_blur_image.shape[0], 1])
        gray_blur_image = np.tile(gray_blur_image, 3)
        return gray_blur_image

    def _create_retina_image(self, image):
        blur_image = self._create_blur_image(image)
        retina_image = image * self.rates + blur_image * self.inv_rates
        return retina_image.astype(np.uint8)
