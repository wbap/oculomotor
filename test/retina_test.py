# -*- coding: utf-8 -*-
import unittest
import os
from skimage import io
import numpy as np
import time

from functions.retina import Retina

class TestRetina(unittest.TestCase):
    def setUp(self):
        self.retina = Retina()

    def get_file_path(self, relative_path):
        abs_path_module = os.path.realpath(__file__)
        module_dir, _ = os.path.split(abs_path_module)
        file_path = os.path.join(module_dir, relative_path)
        return file_path

    def load_image(self, path):
        file_path = self.get_file_path(path)
        image =  io.imread(file_path)
        return image

    def save_image(self, image, path):
        file_path = self.get_file_path(path)
        io.imsave(file_path, image)

    def test_retina_rates(self):
        if not os.path.exists(self.get_file_path("test_results")):
            os.mkdir(self.get_file_path("test_results"))
        
        rates = self.retina.rates
        rates = (rates * 255.0).astype(np.uint8)
        rates = np.reshape(rates, [128,128])
        self.save_image(rates, "test_results/retina_rates.png")

    def test_retina_performance(self):
        image = self.load_image("images/task_images/1_000.png")
        
        start = time.time()
        frame_size = 100
        for i in range(frame_size):
            tmp = self.retina._create_retina_image(image)
        elapsed_time = time.time() - start
        
        print('retina process time: {}[sec]'.format(elapsed_time / frame_size))
        
        

if __name__ == '__main__':
    unittest.main()
