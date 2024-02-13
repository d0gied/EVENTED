# Monorepo Specifications

## Introduction

This document outlines the specifications for this monorepo structure and the tools used to manage the monorepo.

## Table of Contents

...

## Repo structure

```plaintext
/EVENTED                            # Root directory for the entire project
│
├── /libs                           # Documentation files for the project
├── /services                       # Service-specific directories
│   ├── /service                    # Microservice
│   │   ├── /service                # Source code for service
│   │   ├── /tests                  # Test code for service
│   │   ├── pyproject.toml          # Python project configuration
│   │   ├── poetry.lock             # Poetry lock file
│   │   ├── entrypoint.sh           # Entrypoint script for Docker
│   │   └── README.md               # Documentation specific to service
│   │
│   └── /service-n                  # More services...
│
├── /config                         # Configuration files for deployment, env, etc.
│   ├── service.yaml       # Configuration for service
│   ├── service.secret.yaml       # Secret configuration for service
│   └── service.local.yaml       # Local configuration for service
│
├── /scripts                        # Utility scripts, e.g., for deployment or local setup
├── /docker                         # All Docker-related files
│
├── docker-compose.yml              # Docker Compose file to run services locally
├── .gitignore                      # Default gitignore file
└── README.md                       # General documentation for the whole project
```

### Notes on the Structure:

- **/services**: Contains all the individual services that make up your application. Each service has its own source code, dependencies, tests, Dockerfile for containerization, and service-specific documentation.

- **/libs**: This is where the shared libraries or components that multiple services might use are placed. They should be versioned and could be independently released if desired.

## Service Structure

Each service has the following structure:

```plaintext
/service                    # Microservice
│   ├── /service             # Source code for service
│   ├── /tests               # Test code for service
│   ├── pyproject.toml       # Python project configuration
│   ├── poetry.lock          # Poetry lock file
│   ├── entrypoint.sh        # Entrypoint script for Docker
│   └── README.md            # Documentation specific to service
```

All services have the same structure. The `entrypoint.sh` script is used to start the service in the Docker container.

## Shared Libraries

Shared libraries are stored in the `libs` directory. They are versioned and can be independently released if desired.
This allows for code reuse across services and ensures that changes to shared libraries are reflected in all services that use them.

## Tools

### Poetry

Poetry is used to manage the Python dependencies for the services and the shared libraries. It is also used to manage the Python version for the project.

#### Usage

**Install dependencies:**
```bash
# /services/{service_name}
poetry install
```

**Add public library to service:**
```toml
# /services/{service_name}/pyproject.toml
[tool.poetry.dependencies]
lib-name = "^0.1.0"
```

```bash
# /services/{service_name}
poetry lock # to regenerate lock file
poetry install # to install the shared library
```

**OR**

```bash
# /services/{service_name}
poetry add lib-name
```

**Add shared library to service:**
```toml
# /services/{service_name}/pyproject.toml
[tool.poetry.dependencies]
lib-name = { path = "../../libs/lib-name", develop = false }

[tool.poetry.dev-dependencies]
lib-name = { path = "../../libs/lib-name", develop = true }
```

There are two entries for the shared library, one in `dependencies` and one in `dev-dependencies`. `develop` flag is related to the shared library development, if it's set to `true` poetry will just make link to the shared library, if it's set to `false` poetry will install the shared library as a dependency. (`develop=true` allows not to install the shared library on every change of the shared library).

```bash
# /services/{service_name}
poetry lock # to regenerate lock file
poetry install # to install the shared library
```

### Docker

Docker is used to containerize the services and the shared libraries.

There is one `Dockerfile` for all services which is stored in the `docker/service.Dockerfile`.

#### Usage

**Build with docker-compose(Recomended):** 
```bash
# /
docker-compose build {service_name}
```

**Build with Makefile:**
```bash
# /
make build-service service={service_name}
```

**Direct image build:**
```bash
# /
docker build -t evented-{service_name} -f docker/service.Dockerfile . --build-arg SERVICE_NAME={service_name}
```

Build the image for the service. The `SERVICE_NAME` argument is used to copy the service source code into the image. `SERVICE_NAME` should be the same as the name of the service directory(e.g. `database`, without `/service/` prefix).

**Run service with docker-compose(Recomended):**
```bash
# /
docker-compose up {service_name}
```

**Run project with docker-compose:**
```bash
# /
docker-compose up -d
```

### Configuration

[Configuration](../libs/common-utils/README.md#common-utils.config) is managed with the `common-utils` library.

### Scripts

Utility scripts are stored in the `scripts` directory. They are used for deployment or local setup.

### Docker Compose

The `docker-compose.yml` file is used to run the services locally. It is also used to run the entire stack locally.