# -*- coding: utf-8 -*-
import unittest
import os
from skimage import io
import numpy as np
import time
import glob

from functions.lip import LIP
from functions.retina import Retina


class TestLIP(unittest.TestCase):
    def setUp(self):
        self.lip = LIP()
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

    def concat_images(self, images):
        spacer = np.ones([128, 1, 3], dtype=np.uint8)
        images_with_spacers = []

        image_size = len(images)
  
        for i in range(image_size):
            images_with_spacers.append(images[i])
            if i != image_size-1:
                # 1ピクセルのスペースを空ける
                images_with_spacers.append(spacer)
        ret = np.hstack(images_with_spacers)
        return ret

    def convert_to_retina_image(self, image):
        return self.retina._create_retina_image(image)

    def sub_test_saliency_map(self, file_path):
        image = self.load_image(file_path)
        file_base_name = os.path.splitext(os.path.basename(file_path))[0]
        
        retina_image = self.convert_to_retina_image(image)
        
        saliency_map = self.lip._get_saliency_map(retina_image)
        saliency_map = saliency_map[:,:,np.newaxis].repeat(3, axis=2)
        saliency_map = (saliency_map * 255.0).astype(np.uint8)

        ret_image = self.concat_images([image, retina_image, saliency_map])
        self.save_image(ret_image, "test_results/out_{}.png".format(file_base_name))

    def test_saliency_map(self):
        if not os.path.exists(self.get_file_path("test_results")):
            os.mkdir(self.get_file_path("test_results"))
        
        images_dir_path = self.get_file_path("images/task_images")
        
        file_path_list = glob.glob("{}/*.png".format(images_dir_path))
        for file_path in file_path_list:
            self.sub_test_saliency_map(file_path)
            
    def test_saliency_map_performance(self):
        image = self.load_image("images/task_images/1_000.png")
        
        start = time.time()
        frame_size = 100
        for i in range(frame_size):
            tmp = self.lip._get_saliency_map(image)
        elapsed_time = time.time() - start
        
        print('saliency process time: {}[sec]'.format(elapsed_time / frame_size))


if __name__ == '__main__':
    unittest.main()
