# Automatically testing the composition of containers

We want to extend our testing to also include tests that check whether the container cluster as setup by docker compose actually behaves as desired. That is, check if the application is running and working correctly.

This is done by combining docker compose and GitHub actions. We created a [docker-compose.override.yml](../../docker-compose.override.yml) file, which overrides the docker-compose file by creating a fourth service which tests the other services. Basically, the override file overrides existing configurations of the docker-compose file and is configured to only be used in testing. It looks as follows: 

```yaml
# This override is used to run the tests of the app
services:
  plantswap-app:
    command: sh -c "poe deploy"
    #    sh -c "uv sync --all-extras --dev && poe test-run && poe deploy"
    healthcheck:
      test: [ "CMD-SHELL", "python3 -c 'import http.client; conn = http.client.HTTPConnection(\"0.0.0.0\", 8000); conn.request(\"GET\", \"/\"); exit(0) if conn.getresponse().status == 200 else exit(1)'" ]
      interval: 5s
      timeout: 5s
      retries: 5
      start_period: 300s

  test-app:
    build: .
    container_name: test-app
    command: sh -c "uv sync --all-extras --dev && uv run pytest --noconftest app/tests/compose/"
    links:
      - plantswap-app
    depends_on:
      plantswap-app:
        condition: service_healthy
```
The plantswap app service is slightly adapted to have a health check function that can determines when the service is ready to be tested. When that occurs, the test-app service is started which uses the same image as the application but has a different (entry) command. Instead of starting the application, we start the pytest compose tests. For these to work, we to link the application and the test service of course. The GitHub action is now configured to use both the [docker-compose](../../docker-compose.yml) and [docker-compose.override](../../docker-compose.override.yml) file. Furthermore, once the test-app has executed the tests (successfully or not), it will exit with code 0 or 1 depending on the result of the tests. This is then tracked by the GitHub actions workflow and returned as an result of the workflow. The entire workflow as defined in [test_compose.yml](../../.github/workflows/test_compose.yml) is therefore as follows:

```yaml
name: Build and Test with Docker Compose

on: push

jobs:
  docker-compose-test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Set up Poethepoet
        run: pipx install poethepoet

      - name: Start compose with Poethepoet
        run: poe compose-test -d

      - name: Wait for app-test container to finish
        run: |
          while docker ps -q --filter "name=test-app" | grep -q .; do
            sleep 5
          done
          EXIT_CODE=$(docker inspect -f '{{.State.ExitCode}}' test-app)
          echo "EXIT_CODE=$EXIT_CODE" >> "$GITHUB_ENV"

      - name: Check exit code and shut down services
        run: |
          if [ "$EXIT_CODE" -eq 0 ]; then
            echo "Test container exited successfully. Shutting down services."
            poe compose-down
          else
            echo "Test container failed with exit code $EXIT_CODE. Shutting down services."
            poe compose-down
            exit 1
          fi
```
