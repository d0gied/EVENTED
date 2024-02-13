# EVENTED

EVENTED is service that provides a simple and scalable event management system. It has easy-to-use APIs for managing, parsing and subscribing to events.

## Features

- **Event Management**: Create, update, and delete events.
- **Event Parsing**: Parse events and send them to the message broker.
- **Event Subscription**: Subscribe to events and receive notifications when an event is created, updated, or deleted.

## Tech Stack

- **aiogram**: For creating Telegram bots.
- **FastAPI**: For building APIs.
- **Pydantic**: For data validation and settings management using Python type annotations.
- **SQLAlchemy**: For SQL databases.
- **Docker**: For containerization.
- **Kafka/RabbitMQ**: For message broker.
- **MongoDB**: For storing events.
- **PostgreSQL**: For storing user data.
- **Redis**: For caching.


## Repo structure

[read more](docs/monorepo-specs.md#repo-structure)

## Architecture

[Read more](docs/architecture.md)

## Mono-repo Specifications

[Read more](docs/monorepo-specs.md)

## Documentation

For now all documentations are in the libs directories. Each service has its own documentation in the `README.md` file.
Sooner, we will have a separate documentation directory for the whole project.

## Configuration

[Read more](libs/common-utils/README.md#common-utilsconfig)