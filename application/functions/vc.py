import brica

class VC(object):
    def __init__(self):
        self.timing = brica.Timing(2, 1, 0)

    def __call__(self, inputs):
        if 'from_retina' not in inputs:
            raise Exception('VC did not recieve from Retina')

        retina_image = inputs['from_retina']
        
        return dict(to_fef=retina_image,
                    to_pfc=retina_image)
