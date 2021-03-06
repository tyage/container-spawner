from flask import Flask, render_template
import docker
from docker.errors import APIError
import os
import json
import logging
from helpers import random_string, spawner_form, spawn_container_with_random_port, number_of_running_containers

# Environment settings
IMAGE_NAME = os.environ.get('SPAWNER_IMAGE_NAME')
if not IMAGE_NAME:
    raise ValueError("No SPAWNER_IMAGE_NAME set")
CONTAINER_PORT = os.environ.get('SPAWNER_CONTAINER_PORT')
if not CONTAINER_PORT:
    raise ValueError("No SPAWNER_CONTAINER_PORT set")
# hostname of a user access URL
SPAWNER_HOSTNAME = os.environ.get('SPAWNER_HOSTNAME', 'localhost')
SPAWNER_USERNAME_ENV = os.environ.get('SPAWNER_USERNAME_ENV', 'CS_USERNAME')
SPAWNER_PASSWORD_ENV = os.environ.get('SPAWNER_PASSWORD_ENV', 'CS_PASSWORD')
PORT_MIN = int(os.environ.get('SPAWNER_PORT_MIN', 62000))
PORT_MAX = int(os.environ.get('SPAWNER_PORT_MAX', 65000))
TIME_LIMIT = os.environ.get('SPAWNER_TIME_LIMIT', 15 * 60)
SPAWNER_MAX_CONTAINER = int(os.environ.get('SPAWNER_MAX_CONTAINER', -1))
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

    running_containers = number_of_running_containers(client, IMAGE_NAME)
    service_avaialbe = SPAWNER_MAX_CONTAINER <= 0 or running_containers < SPAWNER_MAX_CONTAINER

    return render_template('index.html', form=form, service_available=service_avaialbe)


@app.post("/")
def new_instance():
    running_containers = number_of_running_containers(client, IMAGE_NAME)
    if SPAWNER_MAX_CONTAINER > 0 and running_containers > SPAWNER_MAX_CONTAINER:
        return "Sorry, we are currently unavailable to spawn new instance"

    form = spawner_form(RECAPTCHA_PRIVATE_KEY, RECAPTCHA_PUBLIC_KEY)
    if not form.validate_on_submit():
        return "invalid request"

    args = {
        'detach': True,
        'environment': {},
        **CONTAINER_ARGS
    }
    # override some args with random string
    username = random_string()
    password = random_string()
    args['environment'][SPAWNER_USERNAME_ENV] = username
    args['environment'][SPAWNER_PASSWORD_ENV] = password

    try:
        container, exposed_port = spawn_container_with_random_port(
            docker_client=client,
            image_name=IMAGE_NAME,
            source_port=CONTAINER_PORT,
            port_min=PORT_MIN,
            port_max=PORT_MAX,
            args=args
        )
        app.logger.info('spawned: %s', container.name)
    except APIError as error:
        # failed to spawn container
        app.logger.info('spawn failed: %s', str(error))
        message = 'Failed to spawn continer :( Please try again.'
        return render_template('index.html', form=form, error=message)

    return render_template('index.html', form=form, port=exposed_port, username=username, password=password, host=SPAWNER_HOSTNAME, time_limit=TIME_LIMIT, service_available=True)


if __name__ == '__main__':
    app.run()
