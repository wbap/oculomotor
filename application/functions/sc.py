import brica

class SC(object):
    def __init__(self):
        self.timing = brica.Timing(0, 1, 0)

    def __call__(self, inputs):
        if 'from_fef' not in inputs:
            raise Exception('SC did not recieve from FEF')
        if 'from_bg' not in inputs:
            raise Exception('SC did not recieve from BG')
        return dict(to_environment=None)
