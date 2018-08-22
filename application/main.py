import os
import cv2

from flask import Flask, Response, render_template
from jinja2 import FileSystemLoader
app = Flask(__name__)
app.jinja_loader = FileSystemLoader(os.getcwd() + '/templates')

from agent import Agent
from functions import BG, FEF, LIP, PFC, Retina, SC, VC
from oculoenv import PointToTargetContent, Environment


def create_frame(image, convert_bgr=True):
    if convert_bgr:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
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

def _run_inspector(content):
    from inspector import Inspector

    display_size = (128*4+16, 500)
    inspector = Inspector(content, display_size)

    while True:
        done = inspector.update()
        image = inspector.get_frame()
        
        yield create_frame(image, convert_bgr=False)
        
        if done:
            break


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inspector')
def inspector():
    return render_template('inspector.html')


@app.route('/run')
def run():
    mimetype = 'multipart/x-mixed-replace; boundary=frame'
    content = PointToTargetContent(target_size='small', use_lure=True, lure_size='large')
    return Response(_run(content), mimetype=mimetype)

@app.route('/run_inspector')
def run_inspector():
    mimetype = 'multipart/x-mixed-replace; boundary=frame'
    content = PointToTargetContent(target_size='small', use_lure=True, lure_size='large')
    return Response(_run_inspector(content), mimetype=mimetype)


if __name__ == '__main__':
    app.run()
