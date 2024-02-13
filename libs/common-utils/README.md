# Common utilities for projects

## Adding to service

[Read more](/docs/monorepo-specs.md#add-shared-library-to-service)

## Development

```bash
# /libs/common-utils
poetry install
```

## Documentation

### common-utils.config

This module provides a way to load configuration from /config/{service}.yaml

It supports few override options(from less to more priority):
1. `{service}.yaml` - default configuration **required**.
2. `{service}.{environment}.yaml` - environment configuration (e.g. production, development, test)
3. `{service}.secret.yaml` - secret configuration
4. `{service}.local.yaml` - local configuration

`.secret.yaml`, `.local.yaml` and `{environment}.yaml` are optional.

`secret` and `local` configurations are added to `.gitignore` by default.

#### Usage
    
Best practice is to add `config.py` module into your service and use it to load configuration.

```python
# /services/{service_name}/{service_name}/config.py
from common_utils.config import Config

class DatabaseConfig(Config):
    config_name = "database"
    
    class Mongo:
        host: str
        port: int
        username: str
        password: str
        database: str
    
    mongo: Mongo
    
    class Postgres:
        host: str
        port: int
        username: str
        password: str
        database: str
    
    postgres: Postgres
```

```yaml
# /config/{config_name}.yaml
mongo:
    host: localhost
    port: 27017
    database: test
    username: # username
    password: # password
postgres:
    host: localhost
    port: 5432
    database: test
```

```yaml
# /config/{config_name}.secret.yaml
mongo:
    username: root
    password: root
postgres:
    username: root
    password: root
```

```python
# /services/{service_name}/{service_name}/some_module.py
from .config import DatabaseConfig

config = DatabaseConfig()

print(config.mongo.host) # localhost
print(config.mongo.username) # root

print(config.tree) # print all configuration in yaml format
"""
mongo:
    host: localhost
    port: 27017
    username: root
    password: root
    database: test
postgres:
    host: localhost
    port: 5432
    username: root
    password: root
    database: test
"""
```

**Important**
- Config class is only for type hinting, there is no validation of configuration, no default values and no type casting. Data will be directly loaded from yaml file.

    
