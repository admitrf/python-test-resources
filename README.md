# python-test-resources

Test project [(Google doc)](https://docs.google.com/document/d/12dYhPjwUzzqAbBNEo5X9adTQIJplPR1ApYWM8qtMVYI/edit).

## Available commands

In the project directory, you can run:

### `make build`

Build docker images for backend (Python) and UI (react app). Create containers.

### `make run`

Runs the app in the development mode (docker containers).
Open [http://localhost:3000](http://localhost:3000) to view it in your browser. Or send request to API on [http://localhost:8080/api/v1](http://localhost:8080/api/v1).

### `make stop`

Stop containers.

## `make clean`

 Stop and remove containers and docker network.
