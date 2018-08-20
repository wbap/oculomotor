import os
import cv2

from flask import Flask, Response, render_template
from jinja2 import FileSystemLoader
app = Flask(__name__)
app.jinja_loader = FileSystemLoader(os.getcwd() + '/templates')

from agent import Agent
from functions import BG, FEF, LIP, PFC, Retina, SC, VC
from oculoenv import PointToTargetContent, Environment


def create_frame(image):
    _, jpg = cv2.imencode('.jpg', image)
    data = jpg.tobytes()
    return b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + data + b'\r\n\r\n'


def _run(content):
    agent = Agent(
        retina=Retina(),
        lip=LIP(),
        vc=VC(),
        pfc=PFC(),
        fef=FEF(),
        bg=BG(),
        sc=SC(),
    )

    env = Environment(content)

    obs = env.reset()
    reward = 0
    done = False

    while not done:
        image, angle = obs['screen'], obs['angle']

        yield create_frame(image)

        action = agent(image, angle, reward, done)
        obs, reward, done, _ = env.step(action)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/run')
def run():
    mimetype = 'multipart/x-mixed-replace; boundary=frame'
    content = PointToTargetContent(target_size='small', use_lure=True, lure_size='large')
    return Response(_run(content), mimetype=mimetype)


if __name__ == '__main__':
    app.run()
