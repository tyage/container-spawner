from flask import Flask, render_template
import docker
from docker.errors import APIError
import os
import json
import logging
from helpers import random_port, random_string, spawner_form

# Environment settings
IMAGE_NAME = os.environ.get('SPAWNER_IMAGE_NAME')
if not IMAGE_NAME:
    raise ValueError("No SPAWNER_IMAGE_NAME set")
CONTAINER_PORT = os.environ.get('SPAWNER_CONTAINER_PORT')
if not CONTAINER_PORT:
    raise ValueError("No SPAWNER_CONTAINER_PORT set")
# hostname of a user access URL
SPAWNER_HOSTNAME = os.environ.get('SPAENER_HOSTNAME', 'localhost')
SPAWNER_USERNAME_ENV = os.environ.get('SPAWNER_USERNAME_ENV', 'CS_USERNAME')
SPAWNER_PASSWORD_ENV = os.environ.get('SPAWNER_PASSWORD_ENV', 'CS_PASSWORD')
PORT_MIN = int(os.environ.get('SPAWNER_PORT_MIN', 62000))
PORT_MAX = int(os.environ.get('SPAWNER_PORT_MAX', 65000))
TIME_LIMIT = os.environ.get('SPAWNER_TIME_LIMIT', 15 * 60)
CONTAINER_ARGS = os.environ.get('SPAWNER_CONTAINER_ARGS')
if CONTAINER_ARGS:
    # should be JSON string
    CONTAINER_ARGS = json.loads(CONTAINER_ARGS)
else:
    CONTAINER_ARGS = {}
RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')
SECRET_KEY = os.environ.get("SECRET_KEY")

# Setup app
app = Flask(__name__)
client = docker.from_env()

app.logger.setLevel(logging.INFO)
app.config['SECRET_KEY'] = SECRET_KEY if SECRET_KEY else random_string()

if RECAPTCHA_PUBLIC_KEY and RECAPTCHA_PRIVATE_KEY:
    app.config['RECAPTCHA_PUBLIC_KEY'] = RECAPTCHA_PUBLIC_KEY
    app.config['RECAPTCHA_PRIVATE_KEY'] = RECAPTCHA_PRIVATE_KEY


@app.get("/")
def index():
    form = spawner_form(RECAPTCHA_PRIVATE_KEY, RECAPTCHA_PUBLIC_KEY)
    return render_template('index.html', form=form)


@app.post("/")
def new_instance():
    form = spawner_form(RECAPTCHA_PRIVATE_KEY, RECAPTCHA_PUBLIC_KEY)
    if not form.validate_on_submit():
        return "invalid request"

    args = {
        'detach': True,
        'ports': {},
        'environment': {},
        **CONTAINER_ARGS
    }
    # override some args with random string
    exposed_port = random_port(PORT_MIN, PORT_MAX)
    username = random_string()
    password = random_string()
    args['ports'][CONTAINER_PORT] = exposed_port
    args['environment'][SPAWNER_USERNAME_ENV] = username
    args['environment'][SPAWNER_PASSWORD_ENV] = password

    try:
        container = client.containers.run(IMAGE_NAME, **args)
        app.logger.info('spawned: %s', container.name)
    except APIError as error:
        # failed to spawn container
        app.logger.info('spawn failed: %s', str(error))
        message = 'Failed to spawn continer :( Please try again.'
        return render_template('index.html', form=form, error=message)

    return render_template('index.html', form=form, port=exposed_port, username=username, password=password, host=SPAWNER_HOSTNAME, time_limit=TIME_LIMIT)


if __name__ == '__main__':
    app.run()
