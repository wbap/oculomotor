import numpy as np
import brica


class Environment:
    def __init__(self):
        self._image = None
        self._reward = 0.0
        self._done = False
        self._action = None
        self.timing = brica.Timing(0, 1, 0)

    def __call__(self, inputs):
        self._action = inputs['from_sc']
        return dict(to_retina=self._image, to_bg=(self._reward, self._done))

    def set(self, image, reward, done):
        self._image = image
        self._reward = reward
        self._done = done

    @property
    def action(self):
        if self._action is None:
            return np.array([0.0, 0.0], dtype=np.float32)
        return self._action


class Agent(object):
    connections = [
        ('environment', 'retina'),
        ('environment', 'bg'),
        ('retina', 'lip'),
        ('retina', 'vc'),
        ('lip', 'fef'),
        ('vc', 'pfc'),
        ('vc', 'fef'),
        ('pfc', 'fef'),
        ('pfc', 'bg'),
        ('fef', 'pfc'),
        ('fef', 'sc'),
        ('fef', 'bg'),
        ('bg', 'pfc'),
        ('bg', 'fef'),
        ('bg', 'sc'),
        ('sc', 'environment'),
    ]

    def __init__(self, retina, lip, vc, pfc, fef, bg, sc):
        self.components = {}
        self.scheduler = brica.VirtualTimeScheduler()
        self.environment = Environment()
        self.setup(
            environment=self.environment,
            retina=retina,
            lip=lip,
            vc=vc,
            pfc=pfc,
            fef=fef,
            bg=bg,
            sc=sc,
        )

    def setup(self, **functions):
        for key, function in functions.items():
            self.components[key] = brica.Component(function)
            self.scheduler.add_component(self.components[key], function.timing)

        for origin_name, target_name in self.connections:
            in_port = 'from_{}'.format(origin_name)
            out_port = 'to_{}'.format(target_name)

            self.components[origin_name].make_out_port(out_port)
            self.components[target_name].make_in_port(in_port)

            print('connect {} {}'.format(in_port, out_port))

            brica.connect(self.components[origin_name], out_port, self.components[target_name], in_port)

    def __call__(self, image, reward, done):
        self.environment.set(image, reward, done)
        self.scheduler.step()
        return self.environment.action
