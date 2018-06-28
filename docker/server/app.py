import json
from http import HTTPStatus
import flask
from flask import Flask, request
app = Flask(__name__)

from agent import Agent


class Space(object):
    def __init__(self):
        pass

    def sample(self):
        return 0


space = Space()
agent = Agent(space)


@app.route('/initialize', methods=['GET'])
def reset():
    agent = Agent(space)
    return '', HTTPStatus.NO_CONTENT


@app.route('/step', methods=['POST'])
def step():
    if request.headers['Context-Type'] != 'application/json':
        return 'expected JSON body', HTTPStatus.BAD_REQUEST
    observation, reward, done, _ = request.json
    action = agent(observation, reward, done)
    return flask.jsonify(action), HTTPStatus.OK


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
