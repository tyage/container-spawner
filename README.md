# Container Spawner

## Spawner App

[![build and push spawner](https://github.com/tyage/container-spawner/actions/workflows/push-spawner.yml/badge.svg)](https://github.com/tyage/container-spawner/actions/workflows/push-spawner.yml)

```bash
$ docker run -v /var/run/docker.sock:/var/run/docker.sock --name container-spawner -e SPAWNER_IMAGE_NAME=[YOUR_IMAGE] -e SPAWNER_CONTAINER_PORT=[YOUR_PORT] -p 5000:5000 ghcr.io/tyage/container-spawner:latest
$ open http://localhost:5000
```

## Cleaner App

[![build and push cleaner](https://github.com/tyage/container-spawner/actions/workflows/push-cleaner.yml/badge.svg)](https://github.com/tyage/container-spawner/actions/workflows/push-cleaner.yml)

```bash
$ docker run -v /var/run/docker.sock:/var/run/docker.sock --name container-spawner-cleaner -e SPAWNER_IMAGE_NAME=[YOUR_IMAGE] ghcr.io/tyage/container-spawner-cleaner:latest
```