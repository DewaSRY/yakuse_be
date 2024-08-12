# syntax=docker/dockerfile:1

# Base image
ARG PYTHON_VERSION=3.12.0
FROM python:${PYTHON_VERSION}-alpine AS base

# Set environment variables for Poetry
ENV POETRY_VERSION=1.8


# Install Poetry and dependencies in a build stage
FROM base AS build

# Set working directory
WORKDIR /usr/src/app


# Copy the pyproject.toml and poetry.lock files to the container
COPY pyproject.toml poetry.lock* ./
# Create a virtual environment and install Poetry
RUN python3 -m venv .venv\
    &&pip install -U pip setuptools \
    &&pip install poetry==${POETRY_VERSION} \
    &&poetry install --no-root


# Final stage
FROM base AS final

# Prevents Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# Keeps Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1
ENV APP_DEVELOPMENT=False

ENV VIRTUAL_ENV=/usr/src/app/.venv \
    PATH="/usr/src/app/.venv/bin:$PATH"

# Set working directory
WORKDIR /usr/src/app
#copy the dependency
COPY --from=build /usr/src/app/.venv .venv

# Copy the application code to the container
COPY . /usr/src/app


# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
# Add a non-privileged user
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Switch to the non-privileged user
USER appuser

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["python", "run.py"]
