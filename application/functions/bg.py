import numpy as np
import brica


"""
This is an example implemention of BG (Basal ganglia) module.
You can change this as you like.
"""

class BG(object):
    def __init__(self):
        self.timing = brica.Timing(5, 1, 0)

    def __call__(self, inputs):
        if 'from_environment' not in inputs:
            raise Exception('BG did not recieve from Environment')
        if 'from_pfc' not in inputs:
            raise Exception('BG did not recieve from PFC')
        if 'from_fef' not in inputs:
            raise Exception('BG did not recieve from FEF')

        fef_data = inputs['from_fef']

        accmulator_size = len(fef_data)

        # Set threshold as 0.1 (as dummy test)
        likelihood_thresholds = np.ones([accmulator_size], dtype=np.float32) * 0.3
        
        return dict(to_pfc=None,
                    to_fef=None,
                    to_sc=likelihood_thresholds)
