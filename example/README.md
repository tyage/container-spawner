Run Container Spawner:

```
$ docker compose up
```

You can access Container Spawner web interface in http://localhost:5000:

```
$ open localhost:5000
```

After you click the button `Spawn container`, new deno app spawned and you can access it for 10 minutes.

Each spawned app is protected with each basic auth credentials and not accessible by others.
