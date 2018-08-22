import os
import time
import cv2

from flask import Flask, Response, render_template
from jinja2 import FileSystemLoader
app = Flask(__name__)
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

start = time.time()


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
        done = inspector.update()
        image = inspector.get_frame()
        elapsed = time.time() - start

        if elapsed > 1:
            done = True

        yield create_frame(image, convert_bgr=False)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/run/<int:content_id>')
def run(content_id):
    mimetype = 'multipart/x-mixed-replace; boundary=frame'
    return Response(_run(contents[content_id]), mimetype=mimetype)


@app.route('/ping')
def ping():
    start = time.time()
    return '', HTTPStatus.NO_CONTENT


if __name__ == '__main__':
    app.run()
