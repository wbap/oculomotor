# -*- coding: utf-8 -*-
import unittest
import cv2
import numpy as np
import time

from functions.lip import LIP


class TestLIP(unittest.TestCase):
    def setUp(self):
        self.lip = LIP()

    def __max_grey(self, img):
        # print('max val')
        # print(max(img.reshape(-1, )))
        return max(img.reshape(-1, ))

    def __max_gray_pos(self, img, max_val):
        max_pos = np.where(img == max_val)
#        print('org max_pos: ')
#        print(max_pos)

        result = []
        for x, y in zip(max_pos[0], max_pos[1]):
            result.append((x, y))

#        print('max_pos: ')
#        print(result)
        return result

    def __max_in_center(self, img):
        width, height = img.shape

    def __mark_circle(self, img, centers):
        if img.shape == 2:
            rgb_result = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        else:
            rgb_result = img

        for center in centers:
            rgb_result = cv2.circle(rgb_result, center, 5, (0, 0, 255), 2)
        return rgb_result

    def test_original_image(self):
        img = cv2.imread('./images/img_14_org.png')

        start = time.time()
        result = self.lip(img)
        elapsed_time = time.time() - start
        print('elapsed_time: %s[sec]' % elapsed_time)

        cv2.imwrite('./images/lip_14_org.png', result)

        self.assertEqual(img.shape[:2], result.shape)

        max_grey = self.__max_grey(result)
        max_pos = self.__max_gray_pos(result, max_grey)

        rgb_result = self.__mark_circle(result, max_pos)
        cv2.imwrite('./images/lip_marked_14_org.png', rgb_result)

    def test_blured_image(self):
        img = cv2.imread('./images/img_14_ret.png')

        start = time.time()
        result = self.lip(img)
        elapsed_time = time.time() - start
        print('elapsed_time: %s[sec]' % elapsed_time)

        self.assertEqual(img.shape[:2], result.shape)

        max_grey = self.__max_grey(result)
        max_pos = self.__max_gray_pos(result, max_grey)

        rgb_result = self.__mark_circle(result, max_pos)
        cv2.imwrite('./images/lip_marked_14_ret.png', rgb_result)

    def test_partial_gray_image(self):
        img = cv2.imread('./images/img_14_ret_partial_gray.png')

        start = time.time()
        result = self.lip(img)
        elapsed_time = time.time() - start
        print('elapsed_time: %s[sec]' % elapsed_time)

        cv2.imwrite('./images/lip_14_ret_partial_gray.png', result)

        self.assertEqual(img.shape[:2], result.shape)

        max_grey = self.__max_grey(result)
        max_pos = self.__max_gray_pos(result, max_grey)

        rgb_result = self.__mark_circle(result, max_pos)

        center_img = result[32:96, 32:96]
        center_max_gray = self.__max_grey(center_img)
        center_max_pos = self.__max_gray_pos(center_img, center_max_gray)

        adjust_centers = []
        for center in center_max_pos:
            x = center[0] + 32
            y = center[1] + 32
            adjust_centers.append((x, y))

#        print('max_pos in center area:')
#        print(adjust_centers)
        rgb_result = self.__mark_circle(rgb_result, adjust_centers)
        cv2.imwrite('./images/lip_marked_14_ret_partial_gray.png', rgb_result)


if __name__ == '__main__':
    unittest.main()
