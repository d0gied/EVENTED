# Architecture

## Overview

The architecture of the system is based on the following components:
- **Telegram bot**: The main interface for the user to interact with the system.
- **API**: The main interface for the user to interact with the system programmatically.
- **Message broker**: The system uses a message broker to handle asynchronous communication between services.
- **Databases**: The system uses both SQL and NoSQL databases to store data.
- **Telegram sender**: A service that sends messages to the Telegram bot.
- **Event parsers**: Services that parse events and send them to the message broker.

## Services

The system is composed of the following services:
- **Telegram bot**: The main interface for the user to interact with the system.
- **API**: The main interface for the user to interact with the system programmatically.
- **Telegram sender**: A service that sends messages to the Telegram bot.
- **Event parsers**: Services that parse events and send them to the message broker.
- **Database**: A service that manages the database connection and executes queries.

## Tech Stack

The system uses the following technologies:
- **aiogram**: For creating Telegram bots.
- **FastAPI**: For building APIs.
- **Pydantic**: For data validation and settings management using Python type annotations.
- **SQLAlchemy**: For SQL databases.
- **Docker**: For containerization.
- **RabbitMQ**: For message broker.
- **MongoDB**: For storing events.
- **PostgreSQL**: For storing user data.
- **Redis**: For caching.

## Data Flow

The data flow in the system is as follows:
1. **Event parsing**: Events are parsed and sent to the message broker.
2. **Event processing**: Generating extra parameters, like category, and sending to the message broker.
3. **Saving to database**: Event is saved to the database.
4. **Sending to Telegram**: Event is sent to the Telegram bot.
5. **Timed events**: Events are sent to the message broker at a specific time(a week before the event, a day before the event, etc).