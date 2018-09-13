# -*- coding: utf-8 -*-
import unittest
import cv2
import numpy as np
import time
import os
import shutil


from evaluate import TrialResult, save_results, aggregate_results


class TestEvaluate(unittest.TestCase):
    def get_trial_results(self):
        all_trial_results = []

        all_trial_results.append(TrialResult(content_id=1, difficulty=0,
                                             reward=1,
                                             info=dict(result='success',
                                                       reaction_step=100)))
        all_trial_results.append(TrialResult(content_id=1, difficulty=0,
                                             reward=1,
                                             info=dict(result='success',
                                                       reaction_step=105)))
        all_trial_results.append(TrialResult(content_id=1, difficulty=1,
                                             reward=1,
                                             info=dict(result='success',
                                                       reaction_step=10)))
        all_trial_results.append(TrialResult(content_id=1, difficulty=1,
                                             reward=1,
                                             info=dict(result='success',
                                                       reaction_step=104)))
        all_trial_results.append(TrialResult(content_id=1, difficulty=2,
                                             reward=1,
                                             info=dict(result='success',
                                                       reaction_step=100)))
        all_trial_results.append(TrialResult(content_id=2, difficulty=0,
                                             reward=0,
                                             info=dict(result='fail',
                                                       reaction_step=103)))
        all_trial_results.append(TrialResult(content_id=2, difficulty=2,
                                             reward=0,
                                             info=dict(result='fail',
                                                       reaction_step=100)))
        all_trial_results.append(TrialResult(content_id=2, difficulty=4,
                                             reward=1,
                                             info=dict(result='success',
                                                       reaction_step=102)))
        all_trial_results.append(TrialResult(content_id=3, difficulty=-1,
                                             reward=0,
                                             info=dict(result='fail',
                                                       reaction_step=100)))
        all_trial_results.append(TrialResult(content_id=4, difficulty=0,
                                             reward=0,
                                             info=dict(result='fail',
                                                       reaction_step=100)))
        all_trial_results.append(TrialResult(content_id=4, difficulty=2,
                                             reward=1,
                                             info=dict(result='success',
                                                       reaction_step=100)))
        all_trial_results.append(TrialResult(content_id=3, difficulty=-1,
                                             reward=0,
                                             info=dict(result='fail',
                                                       reaction_step=100)))
        all_trial_results.append(TrialResult(content_id=3, difficulty=-1,
                                             reward=1,
                                             info=dict(result='success',
                                                       reaction_step=101)))
        return all_trial_results
    
    def test_save_results(self):
        all_trial_results = self.get_trial_results()
        save_results(all_trial_results, "test_tmp")
        
    def test_aggregate_results(self):
        all_trial_results = []
        all_trial_results.append(TrialResult(content_id=1, difficulty=0,
                                             reward=1,
                                             info=dict(result='success',
                                                       reaction_step=100)))
        all_trial_results.append(TrialResult(content_id=1, difficulty=0,
                                             reward=0,
                                             info=dict(result='fail',
                                                       reaction_step=200)))
        all_trial_results.append(TrialResult(content_id=1, difficulty=0,
                                             reward=0,
                                             info=dict(result='fail',
                                                       reaction_step=300)))
        
        aggregated_results = aggregate_results(all_trial_results)
        self.assertEqual(aggregated_results[0].get_string(),
                         "1,0,1,3,0.333,200.00")
        # content=1, difficulty=0, reward, trial_count, accuracy, reaction_step
        
        self.assertEqual(aggregated_results[1].get_string(),
                         "1,1,0,0,0.000,0.00")
        # content=1, difficulty=1, reward, trial_count, accuracy, reaction_step

        self.assertEqual(aggregated_results[-1].get_string(),
                         "6,4,0,0,0.000,0.00")
        # content=6, difficulty=4, reward, trial_count, accuracy, reaction_step
        
    def tearDown(self):
        if os.path.exists("test_tmp"):
            shutil.rmtree("test_tmp")
    
if __name__ == '__main__':
    unittest.main()
