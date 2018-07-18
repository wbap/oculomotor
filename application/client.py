# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import requests
import numpy as np

from oculoenv import PointToTargetContent, Environment


def npEncode(obj):
    return {
        'data': obj.tolist(),
        'type': obj.dtype.str,
    }


def npDecode(obj):
    return np.array(obj['data'], dtype=np.dtype(obj['type']))


def check_offscreen():
    content = PointToTargetContent(
        target_size="small", use_lure=True, lure_size="large")
    env = Environment(content)
    url = 'http://127.0.0.1:5000/{}'
    headers = {'Content-Type': 'application/json'}

    frame_size = 60

    reward = 0
    done = False

    obs = env.reset()

    for i in range(frame_size):
        msg = json.dumps([npEncode(obs), reward, done, None])
        res = requests.post(url.format('step'), headers=headers, data=msg)
        action = npDecode(res.json())
        obs, reward, done, _ = env.step(action)

        if done:
            print("Episode terminated")
            obs = env.reset()


def main():
    check_offscreen()


if __name__ == '__main__':
    main()
