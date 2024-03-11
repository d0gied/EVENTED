FROM python:3.11.8-slim as base


ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1

RUN apt-get update && apt-get install --no-install-recommends -y build-essential curl

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Builder stage installs dependencies and copies them to the final image
FROM base as builder

COPY --from=base /opt/poetry /opt/poetry
COPY --from=base /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=base /usr/local/bin /usr/local/bin

ARG SERVICE_NAME

ENV POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PATH="$POETRY_HOME/bin:$PATH" \
    SERVICE_PATH="services/${SERVICE_NAME}"

# Copy only requirements (to leverage Docker cache)
WORKDIR /tmp
COPY ${SERVICE_PATH}/pyproject.toml ${SERVICE_PATH}/poetry.lock* ./
COPY libs/ /libs

# Install dependencies
RUN  poetry install --no-root --no-dev

# Final image copies installed packages from builder
FROM base as final

COPY --from=builder /opt/poetry /opt/poetry
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

ARG SERVICE_NAME

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    PATH="$POETRY_HOME/bin:$PATH" \
    SERVICE_PATH="services/${SERVICE_NAME}" \
    POETRY_VIRTUALENVS_CREATE=false \
    SERVICE_NAME=${SERVICE_NAME}

WORKDIR /app

# Copy the service
COPY services/${SERVICE_NAME} /app/

RUN ["chmod", "+x", "/app/entrypoint.sh"]

# Run the service
CMD ["/app/entrypoint.sh"]