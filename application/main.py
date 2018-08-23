import os
import time
from http import HTTPStatus
import cv2

import flask
from flask import Flask, Response, render_template, send_from_directory, stream_with_context
from jinja2 import FileSystemLoader

app = Flask(__name__, static_url_path='')
app.jinja_loader = FileSystemLoader(os.getcwd() + '/templates')

from oculoenv import PointToTargetContent, Environment
from inspector import Inspector

from oculoenv import PointToTargetContent, ChangeDetectionContent, OddOneOutContent, VisualSearchContent, MultipleObjectTrackingContent, RandomDotMotionDiscriminationContent

contents = [
    PointToTargetContent(
        target_size="small", use_lure=True, lure_size="large"),
    ChangeDetectionContent(
        target_number=2, max_learning_count=20, max_interval_count=10),
    OddOneOutContent(),
    VisualSearchContent(),
    MultipleObjectTrackingContent(),
]


def create_frame(image, convert_bgr=True):
    if convert_bgr:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    _, jpg = cv2.imencode('.jpg', image)
    data = jpg.tobytes()
    return b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + data + b'\r\n\r\n'


def _run(content):
    from inspector import Inspector

    display_size = (128 * 4 + 16, 500)
    inspector = Inspector(content, display_size)

    done = False

    while not done:
        start = flask.g.get('start', time.time())

        elapsed = time.time() - start

        if elapsed > 0.2:
            break

        done = inspector.update()
        image = inspector.get_frame()

        yield create_frame(image, convert_bgr=False)


@app.route('/monitor/<path:path>')
def monitor(path):
    return send_from_directory(os.getcwd() + '/monitor/build', path)


@app.route('/run/<int:content_id>')
def run(content_id):
    mimetype = 'multipart/x-mixed-replace; boundary=frame'
    time.sleep(0.3)
    content = contents[content_id]
    content.reset()
    return Response(_run(stream_with_context(content)), mimetype=mimetype)


@app.route('/ping')
def ping():
    flask.g.start = time.time()
    return '', HTTPStatus.NO_CONTENT


if __name__ == '__main__':
    app.run()
