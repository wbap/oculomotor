import brica

class FEF(object):
    def __init__(self):
        self.timing = brica.Timing(0, 1, 0)

    def __call__(self, inputs):
        if 'from_lip' not in inputs:
            raise Exception('FEF did not recieve from LIP')
        if 'from_vc' not in inputs:
            raise Exception('FEF did not recieve from VC')
        if 'from_pfc' not in inputs:
            raise Exception('FEF did not recieve from PFC')
        if 'from_bg' not in inputs:
            raise Exception('FEF did not recieve from BG')
        return dict(to_pfc=None, to_bg=None, to_sc=None)
