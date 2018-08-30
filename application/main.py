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

app = Flask(__name__, static_url_path='')
app.secret_key = 'oculomotor'
app.jinja_loader = FileSystemLoader(os.getcwd() + '/templates')

contents = [
    PointToTargetContent(),
    ChangeDetectionContent(),
    OddOneOutContent(),
    VisualSearchContent(),
    MultipleObjectTrackingContent(),
    RandomDotMotionDiscriminationContent(),
]

display_size = (128 * 4 + 16, 500)


class Runner(object):
    def __init__(self):
        self.content_id = 0
        self.inspector = Inspector(contents[self.content_id], display_size)
        self.lock = Lock()

    def step(self):
        with self.lock:
            self.inspector.update()
            image = self.inspector.get_frame()
        data = cv2.imencode('.png', image)[1].tobytes()
        encoded = base64.encodestring(data)
        return make_response(encoded)

    def swap(self, content_id):
        with self.lock:
            self.inspector = Inspector(contents[content_id], display_size)
        return 'Switched Content', HTTPStatus.OK

runner = Runner()


@app.route('/step')
def step():
    return runner.step()


@app.route('/swap/<int:content_id>')
def swap(content_id):
    return runner.swap(content_id)


@app.route('/monitor/<path:path>')
def monitor(path):
    return send_from_directory(os.getcwd() + '/monitor/build', path)
