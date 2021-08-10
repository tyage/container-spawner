# Container Spawner

## Spawner App

```bash
$ docker build -t container-spawner spawner
$ docker run -v /var/run/docker.sock:/var/run/docker.sock --name container-spawner container-spawner
```

## Cleaner App

```bash
$ docker build -t container-spawner-cleaner cleaner
$ docker run -v /var/run/docker.sock:/var/run/docker.sock --name container-spawner-cleaner container-spawner-cleaner
```