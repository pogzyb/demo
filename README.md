### Simple API

`simple-api` is a wrapper around the GiantBomb API. Use it to retrieve information about a game from [Giantbomb.com](https://giantbomb.com).

The `search-service` API docs are located at `./search-service/SEARCH-SERVICE.md`.

| Command      | Description |
| ----------- | ----------- |
| `make build-and-run`      | Builds and then starts the container.       |
| `make build-and-tag `   | Builds and then tags the docker container with a given version tag.        |
| `make test `   | Starts the container in detached mode, runs the pytest command in the container, and then brings down the container.        |
| `make run `   | Starts the container.        |
