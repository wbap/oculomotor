import brica

class Retina(object):
    def __init__(self):
        self.timing = brica.Timing(1, 1, 0)

    def __call__(self, inputs):
        if 'from_environment' not in inputs:
            raise Exception('Retina did not recieve from Environment')
        return dict(to_lip=None, to_vc=None)
