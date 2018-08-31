# -*- coding: utf-8 -*-
import unittest
import cv2
import numpy as np
import time
import os

from evaluate import TrialResult, save_results


class TestEvaluate(unittest.TestCase):
    def test_save_results(self):
        all_results = []

        all_results.append(TrialResult(content_id=1, difficulty=0,
                                       info=dict(result='success',
                                                 reaction_step=100)))
        all_results.append(TrialResult(content_id=1, difficulty=0,
                                       info=dict(result='success',
                                                 reaction_step=105)))
        all_results.append(TrialResult(content_id=1, difficulty=1,
                                       info=dict(result='success',
                                                 reaction_step=10)))
        all_results.append(TrialResult(content_id=1, difficulty=1,
                                       info=dict(result='success',
                                                 reaction_step=104)))
        all_results.append(TrialResult(content_id=1, difficulty=2,
                                       info=dict(result='success',
                                                 reaction_step=100)))        
        all_results.append(TrialResult(content_id=2, difficulty=0,
                                       info=dict(result='fail',
                                                 reaction_step=103)))
        all_results.append(TrialResult(content_id=2, difficulty=2,
                                       info=dict(result='fail',
                                                 reaction_step=100)))
        all_results.append(TrialResult(content_id=2, difficulty=5,
                                       info=dict(result='success',
                                                 reaction_step=102)))
        all_results.append(TrialResult(content_id=3, difficulty=-1,
                                       info=dict(result='fail',
                                                 reaction_step=100)))
        all_results.append(TrialResult(content_id=4, difficulty=0,
                                       info=dict(result='fail',
                                                 reaction_step=100)))
        all_results.append(TrialResult(content_id=4, difficulty=2,
                                       info=dict(result='success',
                                                 reaction_step=100)))
        all_results.append(TrialResult(content_id=4, difficulty=-1,
                                       info=dict(result='fail',
                                                 reaction_step=100)))
        all_results.append(TrialResult(content_id=4, difficulty=-1,
                                       info=dict(result='success',
                                                 reaction_step=101)))
        
        save_results(all_results, "tmp")
        
    
if __name__ == '__main__':
    unittest.main()
