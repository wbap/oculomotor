import brica

class VC(object):
    """ Visual Cortex module.
    
    You can add feature extraction code as like if needed.
    """
    
    def __init__(self):
        self.timing = brica.Timing(2, 1, 0)

    def __call__(self, inputs):
        if 'from_retina' not in inputs:
            raise Exception('VC did not recieve from Retina')
        
        retina_image = inputs['from_retina']

        # Current implementation just passes through input retina image to FEF and PFC.
        
        return dict(to_fef=retina_image,
                    to_pfc=retina_image)
