import brica

class LIP(object):
    def __init__(self):
        self.timing = brica.Timing(0, 1, 0)

    def __call__(self, inputs):
        if 'from_retina' not in inputs:
            raise Exception('LIP did not recieve from Retina')
        return dict(to_fef=None)
