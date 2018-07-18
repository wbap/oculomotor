from http import HTTPStatus

import numpy as np

import flask
from flask import Flask, request
app = Flask(__name__)

from agent import Agent
from functions.retina import Retina
from functions.lip import LIP
from functions.it import IT
from functions.working_memory import WorkingMemory
from functions.pattern_matcher import PatternMatcher
from functions.state_manager import StateManager
from functions.fef import FEF


agent = Agent(Retina(), LIP(), IT(), WorkingMemory(), PatternMatcher(), StateManager(), FEF())


def npEncode(obj):
    return {
        'data': obj.tolist(),
        'type': obj.dtype.str,
    }


def npDecode(obj):
    return np.array(obj['data'], dtype=np.dtype(obj['type']))


@app.route('/initialize', methods=['GET'])
def reset():
    agent = Agent(Retina(), LIP(), IT(), WorkingMemory(), PatternMatcher(), StateManager(), FEF())
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
