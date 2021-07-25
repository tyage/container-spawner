# Container Spawner

## Spawner App

```bash
$ cd sapwner
$ docker build -t container-spawner .
$ docker run -v /var/run/docker.sock:/var/run/docker.sock --name container-spawner container-spawner
```

## Cleaner App

```bash
$ cd cleaner
$ docker build -t container-spawner-cleaner .
$ docker run -v /var/run/docker.sock:/var/run/docker.sock --name container-spawner-cleaner container-spawner-cleaner
```