# -*- coding: utf-8 -*-
import unittest
import cv2
import numpy as np
import time
import os


class TestTemplateMatch(unittest.TestCase):
    def get_file_path(self, rel_path):
        # このファイルに対する相対パスから絶対パスに変換
        abs_path_module = os.path.realpath(__file__)
        module_dir, _ = os.path.split(abs_path_module)
        abs_path = os.path.join(module_dir, rel_path)
        return abs_path
    
    
    def process_template_matching(self, obs, template_img):
        # テンプレートマッチング処理
        res = cv2.matchTemplate(obs, template_img, cv2.TM_CCOEFF_NORMED)
        # resは、(118, 118) np.float32
        
        # resの中の最大値の場所と位置を探してくる
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        
        # テンプレートマッチングでは、画像の左上ピクセルの座標で結果が返ってくるので、中心の座標に直す.
        half_h = template_img.shape[0] // 2
        half_w = template_img.shape[1] // 2
        max_center_loc = (max_loc[0] + half_w, max_loc[1] + half_h)

        # 最大だった座標とマッチング値を返す
        return max_center_loc, max_val
    
    def test_template_matching(self):
        # テンプレートマッチングのサンプル
        
        # テンプレート画像のロード
        template_img = cv2.imread(self.get_file_path("./images/tm_template.png"))
        # (11, 11, 3), np.uint8
        
        # 入力画像ダミーをロード
        obs          = cv2.imread(self.get_file_path("./images/tm_input.png"))
        # (128, 128, 3), np.uint8
        
        # テンプレートマッチングの実行
        match_pos, match_value = self.process_template_matching(obs, template_img)
        print(match_pos) #..
        
        # マッチ座標
        self.assertEqual(len(match_pos), 2)
        self.assertTrue(0 <= match_pos[0] < obs.shape[1]) # x座標
        self.assertTrue(0 <= match_pos[1] < obs.shape[0]) # y座標
        
        # マッチValue
        self.assertTrue(0.0 <= match_value < 1.0) # 0.0~1.0の値
        
        
        
        
if __name__ == '__main__':
    unittest.main()
    
