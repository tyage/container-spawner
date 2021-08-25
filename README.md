# Container Spawner

A web app which provides private and temporary containers for visitors.

Container Spawner publish containers with random port and generate random password to access them.

Need an example?
Try [this sample app](./example/).

## Spawner App

[![build and push spawner](https://github.com/tyage/container-spawner/actions/workflows/push-spawner.yml/badge.svg)](https://github.com/tyage/container-spawner/actions/workflows/push-spawner.yml)

```bash
$ docker run -v /var/run/docker.sock:/var/run/docker.sock -e SPAWNER_IMAGE_NAME=[YOUR_IMAGE] -e SPAWNER_CONTAINER_PORT=[YOUR_PORT] -p 5000:5000 ghcr.io/tyage/container-spawner:latest
$ open http://localhost:5000
```

You can update configuration with environments

|Env|Description|Default Value|
|-|-|-|
|SPAWNER_IMAGE_NAME (*required*)|Name of the image you want to run.||
|SPAWNER_CONTAINER_PORT (*required*)|Container port you want to expose. Random host port will be assigned to each containers.||
|SPAENER_HOSTNAME|Hostname of the URL shown to user.|localhost|
|SPAWNER_USERNAME_ENV|Container receives the random username with this environment.|CS_USERNAME|
|SPAWNER_PASSWORD_ENV|Container receives the random password with this environment.|CS_PASSWORD|
|SPAWNER_PORT_MIN|Min random port.|62000|
|SPAWNER_PORT_MAX|Max random port.|65000|
|SPAWNER_TIME_LIMIT|Life time of the spawned container.|900|
|SPAWNER_CONTAINER_ARGS|JSON string which represents [parameters for running container](https://docker-py.readthedocs.io/en/stable/containers.html). e.g. `{"environment":{"NODE_ENV":"production"}}`||
|RECAPTCHA_PUBLIC_KEY|Recaptcha site key.||
|RECAPTCHA_PRIVATE_KEY|Recaptcha secret key.||

## Cleaner App

[![build and push cleaner](https://github.com/tyage/container-spawner/actions/workflows/push-cleaner.yml/badge.svg)](https://github.com/tyage/container-spawner/actions/workflows/push-cleaner.yml)

```bash
$ docker run -v /var/run/docker.sock:/var/run/docker.sock -e SPAWNER_IMAGE_NAME=[YOUR_IMAGE] ghcr.io/tyage/container-spawner-cleaner:latest
```

You can update configuration with environments

|Env|Description|Default Value|
|-|-|-|
|SPAWNER_IMAGE_NAME (*required*)|Name of the image you want to stop after the time limit.||
|SPAWNER_TIME_LIMIT|Life time of the spawned container.|900|
