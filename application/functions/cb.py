import brica
import numpy as np

class CB(object):
    """ Cerebellum module.
    
    CB outputs action for smooth pursuit eye movment.
    """
    def __init__(self):
        self.timing = brica.Timing(5, 1, 0)

    def __call__(self, inputs):
        if 'from_fef' not in inputs:
            raise Exception('CB did not recieve from FEF')

        #fef_data = inputs['from_fef']
        
        action = np.array([0, 0], dtype=np.float32)

        # Action values should be within range [-1.0~1.0]
        return dict(to_environment=action)
