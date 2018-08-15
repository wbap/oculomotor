import brica

class PFC(object):
    def __init__(self):
        self.timing = brica.Timing(3, 1, 0)

    def __call__(self, inputs):
        retina_image = inputs['from_vc']
        
        if 'from_vc' not in inputs:
            raise Exception('PFC did not recieve from VC')
        if 'from_fef' not in inputs:
            raise Exception('PFC did not recieve from FEF')
        if 'from_bg' not in inputs:
            raise Exception('PFC did not recieve from BG')
        return dict(to_fef=None,
                    to_bg=None)
