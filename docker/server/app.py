from http import HTTPStatus

import numpy as np

import flask
from flask import Flask, request
app = Flask(__name__)

from agent import Agent


class Space(object):
    def __init__(self):
        pass

    def sample(self):
        dx = np.random.uniform(low=-0.02, high=0.02)
        dy = np.random.uniform(low=-0.02, high=0.02)
        return np.array([dx, dy])


space = Space()
agent = Agent(space)


def npEncode(obj):
    return {
        'data': obj.tolist(),
        'type': obj.dtype.str,
    }


def npDecode(obj):
    return np.array(obj['data'], dtype=np.dtype(obj['type']))


@app.route('/initialize', methods=['GET'])
def reset():
    agent = Agent(space)
    return '', HTTPStatus.NO_CONTENT


@app.route('/step', methods=['POST'])
def step():
    if request.headers['Content-Type'] != 'application/json':
        return 'expected JSON body', HTTPStatus.BAD_REQUEST
    obs, reward, done, _ = request.json
    action = agent(npDecode(obs), reward, done)
    return flask.jsonify(npEncode(action)), HTTPStatus.OK


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
