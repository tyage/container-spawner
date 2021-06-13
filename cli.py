from flask import Flask
import docker
import os
import time
from dateutil import parser
from datetime import datetime, timezone

app = Flask(__name__)
client = docker.from_env()

IMAGE_NAME = os.environ.get('SPAWNER_IMAGE_NAME')
if not IMAGE_NAME:
    raise ValueError("No SPAWNER_IMAGE_NAME set")
TIME_LIMIT = os.environ.get('SPAWNER_TIME_LIMIT', 15 * 60)

def kill_containers():
    containers = client.containers.list(
      all=True,
      filters={'ancestor':IMAGE_NAME}
    )
    for container in containers:
        try:
            # skip if container is younger than TIME_LIMIT
            created_string = container.attrs['Created']
            created_time = parser.parse(created_string)
            now = datetime.now(created_time.tzinfo)
            diff = (now - created_time).total_seconds()
            if diff < TIME_LIMIT:
                continue

            if container.status != 'exited':
                container.kill()
            container.remove()
        except:
            print("Failed to kill container", container.name)
            True

@app.cli.command("auto-gc")
def auto_gc_containers():
    while True:
        kill_containers()
        time.sleep(1)
