# -*- coding: utf-8 -*-
import unittest
import os
from skimage import io
import numpy as np
import time

from functions.lip import LIP


class TestLIP(unittest.TestCase):
    def setUp(self):
        self.lip = LIP()

    def load_image(self, path):
        abs_path_module = os.path.realpath(__file__)
        module_dir, _ = os.path.split(abs_path_module)
        file_path = os.path.join(module_dir, path)
        image =  io.imread(file_path)
        return image        

    def save_image(self, image, path):
        abs_path_module = os.path.realpath(__file__)
        module_dir, _ = os.path.split(abs_path_module)
        file_path = os.path.join(module_dir, path)
        io.imsave(file_path, image)

    def test_saliency_map(self):
        image = self.load_image("images/lip_image0.png")
        
        start = time.time()
        
        saliency_map = self.lip._get_saliency_map(image)
        
        print(saliency_map)
        
        elapsed_time = time.time() - start
        print('elapsed_time: {}[sec]'.format(elapsed_time))
        
        self.save_image(saliency_map, "images/saliency_result0.png")
        
        

if __name__ == '__main__':
    unittest.main()
