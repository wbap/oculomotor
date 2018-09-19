# -*- coding: utf-8 -*-
"""
 Main script for web monitor interface. 
"""

import os
import time
import base64
from threading import Lock
from http import HTTPStatus

import cv2

from oculoenv import PointToTargetContent, ChangeDetectionContent, OddOneOutContent, VisualSearchContent, MultipleObjectTrackingContent, RandomDotMotionDiscriminationContent
from inspector import Inspector

import flask
from flask import Flask, make_response, send_from_directory
from jinja2 import FileSystemLoader
from werkzeug.local import Local, LocalManager
from flask_cors import CORS

app = Flask(__name__, static_url_path='')
CORS(app)
app.secret_key = 'oculomotor'
app.jinja_loader = FileSystemLoader(os.getcwd() + '/templates')

contents = [
    PointToTargetContent,
    ChangeDetectionContent,
    OddOneOutContent,
    VisualSearchContent,
    MultipleObjectTrackingContent,
    RandomDotMotionDiscriminationContent,
]

display_size = (128 * 4 + 16, 500)


class Runner(object):
    def __init__(self):
        self.content_id = 0
        self.difficulty = -1
        self.inspector = Inspector(contents[self.content_id](-1), display_size)
        self.lock = Lock()

    def init(self):
        self.set_content(0)
        self.set_difficulty(-1)
        return self.info()

    def info(self):
        return flask.jsonify({
            'content_range': len(contents),
            'content': self.content_id,
            'difficulty_range': contents[self.content_id].difficulty_range,
            'difficulty': self.difficulty,
        })

    def step(self):
        with self.lock:
            self.inspector.update()
            image = self.inspector.get_frame()
        data = cv2.imencode('.png', image)[1].tobytes()
        encoded = base64.encodestring(data)
        return make_response(encoded)

    def set_content(self, content_id):
        with self.lock:
            self.content_id = content_id
            content = contents[self.content_id](self.difficulty)
            self.inspector = Inspector(content, display_size)
            ret = {
                'difficulty_range': contents[content_id].difficulty_range,
                'difficulty': -1,
            }
            return flask.jsonify(ret)

    def set_difficulty(self, difficulty):
        with self.lock:
            self.difficulty = difficulty
            content = contents[self.content_id](self.difficulty)
            self.inspector = Inspector(content, display_size)
        return 'New Content Created', HTTPStatus.OK


runner = Runner()


@app.route('/init')
def init():
    return runner.init()


@app.route('/info')
def info():
    return runner.info()


@app.route('/step')
def step():
    return runner.step()


@app.route('/content/<int:content_id>')
def content(content_id):
    return runner.set_content(content_id)

@app.route('/difficulty/<difficulty>')
def difficulty(difficulty):
    return runner.set_difficulty(int(difficulty))


@app.route('/monitor/<path:path>')
def monitor(path):
    return send_from_directory(os.getcwd() + '/monitor/build', path)
