from http import HTTPStatus

import numpy as np

import flask
from flask import Flask, request
app = Flask(__name__)

from agent import Agent

from functions import BG, FEF, LIP, PFC, Retina, SC, VC


agent = Agent(retina=Retina(),
              lip=LIP(),
              vc=VC(),
              pfc=PFC(),
              fef=FEF(),
              bg=BG(),
              sc=SC())


def npEncode(obj):
    return {
        'data': obj.tolist(),
        'type': obj.dtype.str,
    }


def npDecode(obj):
    return np.array(obj['data'], dtype=np.dtype(obj['type']))


@app.route('/initialize', methods=['GET'])
def reset():
    agent = Agent(BG(), FEF(), LIP(), PFC(), Retina(), SC(), VC())
    return '', HTTPStatus.NO_CONTENT


@app.route('/step', methods=['POST'])
def step():
    if request.headers['Content-Type'] != 'application/json':
        return 'expected JSON body', HTTPStatus.BAD_REQUEST
    image, angle, reward, done, _ = request.json
    action = agent(npDecode(image), angle, reward, done)
    return flask.jsonify(npEncode(action)), HTTPStatus.OK
