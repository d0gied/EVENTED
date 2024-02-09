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

```plaintext
/EVENTED                            # Root directory for the entire project
│
├── /docs                           # Documentation files for the project
│   ├── architecture.md             # High-level architecture documentation
│   └── api-specifications          # API specifications for each service
│
├── /services                       # Service-specific directories
│   ├── /service                    # Microservice
│   │   ├── /service                # Source code for service
│   │   ├── /tests                  # Test code for service
│   │   ├── Dockerfile              # Dockerfile for service
│   │   ├── .env.example            # Example environment variables
│   │   ├── pyproject.toml          # Python project configuration
│   │   └── README.md               # Documentation specific to service
│   │
│   └── /service-n                  # More services...
│
├── /libs                           # Shared libraries and components
│   ├── /common-utils               # Common utilities used across services
│   │   ├── /src                    # Source code for common utilities
│   │   └── /tests                  # Tests for common utilities
│   │
│   ├── /message-broker-interface   # Shared message broker interface code
│   │   ├── /src                    # Source code for message broker integration
│   │   └── /tests                  # Tests for message broker integration
│   │
│   └── /more-libraries             # More shared libraries...
│
├── /config                         # Configuration files for deployment, env, etc.
│   ├── service-a-config.yaml       # Configuration for service A
│   ├── service-b-config.yaml       # Configuration for service B
│   └── message-broker-config.yaml  # Configuration for the message broker (e.g., topics)
│
├── /scripts                        # Utility scripts, e.g., for deployment or local setup
│
├── /infrastructure                 # Infrastructure as code for provisioning resources
│   ├── /kubernetes                 # Kubernetes manifests or Helm charts
│   └── /terraform                  # Terraform modules for cloud resources
│
├── docker-compose.yml              # Docker Compose file to run services locally
├── .gitignore                      # Default gitignore file
└── README.md                       # General documentation for the whole project
```

### Notes on the Structure:

- **/services**: Contains all the individual services that make up your application. Each service has its own source code, dependencies, tests, Dockerfile for containerization, and service-specific documentation.

- **/libs**: This is where the shared libraries or components that multiple services might use are placed. They should be versioned and could be independently released if desired.

- **/config**: Global configurations that might be used by CI/CD pipelines or during deployment are stored here. This should include the message broker configurations, such as topics, queues, and any other related configurations.

- **/infrastructure**: Infrastructure as code (IaC) for provisioning the required infrastructure on cloud providers or on-premises environments.

- **/docs**: Important project-wide documentation, including architecture diagrams, API specifications, and other relevant guides.

- **/scripts**: Scripts useful for development, deployment, or operational tasks. These might include database migration scripts, build scripts, or scripts to start/stop the entire stack locally.

- **CI/CD files**: These should include definitions for your continuous integration and deployment pipelines, specifying the jobs, stages, and actions for test, build, and deploy processes.

- **Root-level files**: The root level usually contains README.md, LICENSE, .gitignore, docker-compose.yml (useful for local development environments), and any other configuration files needed at the project level.

Remember, the key to a successful monorepo is maintaining consistency across all the components. This includes similar naming conventions, code styles, and README structures, which will make it easier for developers to understand and work within the repo.
