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
