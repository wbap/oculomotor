import brica

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
        return dict(to_pfc=None, to_fef=None, to_sc=None)
