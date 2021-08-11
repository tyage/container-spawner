from flask import Flask, render_template
import docker
import os
import random
import string

app = Flask(__name__)
client = docker.from_env()

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

def random_port():
    # TODO: exclude used port
    return random.randint(PORT_MIN, PORT_MAX)

def random_string(length: int = 16):
    letters = string.ascii_letters + string.digits
    return "".join(random.sample(string.ascii_letters, length))

@app.get("/")
def index():
    return render_template('index.html')

@app.post("/")
def new_instance():
    # TODO: check recaptcha
    exposed_port = random_port()
    username = random_string()
    password = random_string()
    container = client.containers.run(IMAGE_NAME,
        detach=True,
        ports={
            CONTAINER_PORT: exposed_port,
        },
        environment={
            SPAWNER_USERNAME_ENV: username,
            SPAWNER_PASSWORD_ENV: password
        })
    return render_template('index.html', port=exposed_port, username=username, password=password, host=SPAWNER_HOSTNAME, time_limit=TIME_LIMIT)
