# Based on https://github.com/astral-sh/uv-docker-example/blob/main/standalone.Dockerfile

# First install dependencies with UV in a builder image
FROM debian:13.6-slim AS builder

# Copy uv dependencies instead of linking to cache because cache folder is ephemeral
ENV UV_LINK_MODE=copy

# Precompile Python bytecode to improve cold start times
ENV UV_COMPILE_BYTECODE=1

# Omit development dependencies
ENV UV_NO_DEV=1

# Configure the Python directory so it is consistent
ENV UV_PYTHON_INSTALL_DIR=/python

# Only use the managed Python version
ENV UV_PYTHON_PREFERENCE=only-managed

WORKDIR /roboglance-api

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.12.5  /uv /bin/

# Install Python
COPY .python-version .python-version
RUN uv python install

# Install dependencies
COPY pyproject.toml pyproject.toml
COPY uv.lock uv.lock
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project

# Install project
COPY app app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

# Create a new image that contains the app and dependencies without uv
FROM debian:13.6-slim

# Setup a non-root user
RUN groupadd --system --gid 999 nonroot \
 && useradd --system --gid 999 --uid 999 --create-home nonroot

# Copy the Python version
COPY --from=builder /python /python

# Copy the application from the builder
COPY --from=builder --chown=nonroot:nonroot /roboglance-api /roboglance-api

# Place executables in the environment at the front of the path
ENV PATH="/roboglance-api/.venv/bin:$PATH"

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

# Use the non-root user to run our application
USER nonroot

# Use `/roboglance-api` as the working directory
WORKDIR /roboglance-api

# Run the FastAPI application by default
CMD ["fastapi", "run", "--host", "0.0.0.0"]