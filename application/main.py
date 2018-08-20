import cv2

from flask import Flask, Response, render_template
app = Flask(__name__)

from agent import Agent
from functions import BG, FEF, LIP, PFC, Retina, SC, VC
from oculoenv import PointToTargetContent, Environment


running = False


def create_frame(image):
    data = cv2.imencode('.jpg', image)
    return (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + data + '\r\n\r\n')


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

    while running or not done:
        image, angle = obs['screen'], obs['angle']

        yield create_frame(image)

        action = agent(image, angle, reward, done)
        obs, reward, done, _ = env.step(action)


@app.route('/')
def index():
    return render_template('templates/index.html')


@app.route('/run')
def run():
    mimetype = 'multipart/x-mixed-replace; boundary=frame'
    content = PointToTargetContent(target_size='small', use_lure=True, lure_size='large')
    return Response(_run(content), mimetype=mimetype)


if __name__ == '__main__':
    app.run()
