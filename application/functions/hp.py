import brica

class HP(object):
    """ Hippocampal formation module.

    Create allocentric panel image.
    """
    
    def __init__(self):
        self.timing = brica.Timing(2, 1, 0)
        
    def __call__(self, inputs):
        if 'from_environment' not in inputs:
            raise Exception('HP did not recieve from Environment')

        # This image input from environment is a kind of cheat and not biologically
        # acculate.
        image, angle = inputs['from_environment'] # (128, 128, 3), (2)
        
        map_image = None
        
        return dict(to_pfc=map_image)
