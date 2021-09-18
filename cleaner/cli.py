import docker
import os
import time
from dateutil import parser
from datetime import datetime, timezone

from docker.client import DockerClient


def kill_containers(client: DockerClient, image_name: str, time_limit: int):
    try:
        containers = client.containers.list(
            all=True,
            filters={'ancestor': image_name}
        )
    except:
        print("Failed to fetch containers... try again later...")
        return True

    for container in containers:
        try:
            # skip if container is younger than time limit
            created_string = container.attrs['Created']
            created_time = parser.parse(created_string)
            now = datetime.now(created_time.tzinfo)
            diff = (now - created_time).total_seconds()
            if diff < time_limit:
                continue

            print("Try to kill container", container.name)
            if container.status != 'exited':
                container.kill()
            container.remove()
            print("Done", container.name)
        except:
            print("Failed to kill container. Try remove.", container.name)
            try:
                container.remove()
            except:
                True


if __name__ == '__main__':
    client = docker.from_env()

    image_name = os.environ.get('SPAWNER_IMAGE_NAME')
    if not image_name:
        raise ValueError("No SPAWNER_IMAGE_NAME set")
    time_limit = int(os.environ.get('SPAWNER_TIME_LIMIT', 15 * 60))

    while True:
        kill_containers(client, image_name, time_limit)
        time.sleep(1)
