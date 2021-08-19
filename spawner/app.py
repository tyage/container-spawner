from flask import Flask, render_template
from flask_wtf import FlaskForm, RecaptchaField
import docker
import os
import random
import string
import json

# Environment settings
IMAGE_NAME = os.environ.get('SPAWNER_IMAGE_NAME')
if not IMAGE_NAME:
    raise ValueError("No SPAWNER_IMAGE_NAME set")
CONTAINER_PORT = os.environ.get('SPAWNER_CONTAINER_PORT')
if not CONTAINER_PORT:
    raise ValueError("No SPAWNER_CONTAINER_PORT set")
SPAWNER_HOSTNAME = os.environ.get('SPAENER_HOSTNAME', 'localhost') # hostname of a user access URL
SPAWNER_USERNAME_ENV = os.environ.get('SPAWNER_USERNAME_ENV', 'CS_USERNAME')
SPAWNER_PASSWORD_ENV = os.environ.get('SPAWNER_PASSWORD_ENV', 'CS_PASSWORD')
PORT_MIN = os.environ.get('SPAWNER_PORT_MIN', 62000)
PORT_MAX = os.environ.get('SPAWNER_PORT_MAX', 65000)
TIME_LIMIT = os.environ.get('SPAWNER_TIME_LIMIT', 15 * 60)
CONTAINER_ARGS = os.environ.get('SPAWNER_CONTAINER_ARGS') # should be JSON string
if CONTAINER_ARGS:
    CONTAINER_ARGS = json.loads(CONTAINER_ARGS)
else:
    CONTAINER_ARGS = {}
RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')

# Utilities
def random_port():
    # TODO: exclude used port
    return random.randint(PORT_MIN, PORT_MAX)

def random_string(length: int = 16):
    letters = string.ascii_letters + string.digits
    return "".join(random.sample(string.ascii_letters, length))

class SpawnerForm(FlaskForm):
    if RECAPTCHA_PUBLIC_KEY and RECAPTCHA_PRIVATE_KEY:
        recaptcha = RecaptchaField()

# Setup app
app = Flask(__name__)
client = docker.from_env()

app.config['SECRET_KEY'] = random_string()

if RECAPTCHA_PUBLIC_KEY and RECAPTCHA_PRIVATE_KEY:
    app.config['RECAPTCHA_PUBLIC_KEY'] = RECAPTCHA_PUBLIC_KEY
    app.config['RECAPTCHA_PRIVATE_KEY'] = RECAPTCHA_PRIVATE_KEY

@app.get("/")
def index():
    form = SpawnerForm()
    return render_template('index.html', form=form)

@app.post("/")
def new_instance():
    form = SpawnerForm()
    if not form.validate_on_submit():
        return "invalid request"

    exposed_port = random_port()
    username = random_string()
    password = random_string()
    args = {
        'detach': True,
        'ports': {
            CONTAINER_PORT: exposed_port,
        },
        'environment': {
            SPAWNER_USERNAME_ENV: username,
            SPAWNER_PASSWORD_ENV: password
        },
        **CONTAINER_ARGS
    }
    container = client.containers.run(IMAGE_NAME, **args)
    return render_template('index.html', form=form, port=exposed_port, username=username, password=password, host=SPAWNER_HOSTNAME, time_limit=TIME_LIMIT)

if __name__ == '__main__':
    app.run()
