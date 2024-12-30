# Dockerfile in-depth explanation

To explain the dockerfile, we will go through the contents of the [Dockerfile](../../Dockerfile) line-by-line. The dockerfile is based on the [example](https://github.com/astral-sh/uv-docker-example) given by [uv](https://github.com/astral-sh/uv) since we use uv as our package manager.

The entire dockerfile looks as follows:
```Dockerfile
# Based on https://github.com/astral-sh/uv-docker-example
# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Install the project into `/PlantSwap`
WORKDIR /PlantSwap

# Enable bytecode compilation (for uv)
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Install poethepoet for starting the application
RUN pip install poethepoet

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
ADD pyproject.toml LICENSE log_config.json README.md uv.lock ./
ADD app app

# Install the project's dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev 

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Create a directory for reports
RUN mkdir reports

# Reset the entrypoint (don't invoke `uv` as the base image would)
ENTRYPOINT []

# Run the application using poethepoet
CMD ["poe", "deploy"]
```

As a base image, we use an image provided by uv that is optimized for usage with projects that use uv as the package manager. More precisely, it allows for even better reproducibility, since the local uv cache is transferred into the container to synchronize the project's dependencies.

Furthermore, we set some environment variables that optimize the aforementioned reproducibility and compatibility of the base image. Before syncing the dependencies, we install poethepoet, the task runner used for this project, to guarantee the desired deployment commands/configuration.

The installation of the dependencies is separated into two steps. That is, `uv sync` is called twice. This is done for optimal layering/caching for the docker image. Since the dependencies are installed (once) before the actual project code is added to the image, this ensures that when changes to the project's source code are made, the dependencies will not have to be reinstalled. After adding the project's source code, the dependencies are synced again and the `PATH` environment variable is adapted according to the project's necessities.

In the last steps, a directory for the logs is created, the entrypoint of the base image is reset, and the cmd for starting the application is set using the task runner poethepoet.
