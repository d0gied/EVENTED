# Common utilities for projects

## Adding to service

[Read more](/docs/monorepo-specs.md#add-shared-library-to-service)

## Usage

```python
from common_utils import ... # import what you need
```

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
from common_utils.config import ConfigLoader

loader = ConfigLoader("service_name")

class DatabaseConfig:
    class mongo:
        host: str = loader.Field("mongo.host", env="MONGO_HOST")
        port: int = loader.Field("mongo.port", env="MONGO_PORT")
        username: str = loader.Field("mongo.username", env="MONGO_USERNAME")
        password: str = loader.Field("mongo.password", env="MONGO_PASSWORD")
        database: str = loader.Field("mongo.database", env="MONGO_DATABASE")
    
    class postgres:
        host: str = loader.Field("postgres.host", env="POSTGRES_HOST")
        port: int = loader.Field("postgres.port", env="POSTGRES_PORT")
        username: str = loader.Field("postgres.username", env="POSTGRES_USERNAME")
        password: str = loader.Field("postgres.password", env="POSTGRES_PASSWORD")
        database: str = loader.Field("postgres.database", env="POSTGRES_DATABASE")
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
```
    
## Celery

Celery is used for asynchronous task processing. It is used to handle long-running tasks such as sending emails, generating reports, and other background tasks.

### Workflow

1. Add shared task to the `common-utils` library.
2. Take the shared task from the `common-utils` library and implement it in the service.
3. Add the task to the `celery` worker in the service.

### Usage

**Start celery worker:**
```bash
# /services/{service_name}
celery -A service worker --loglevel=info
```

**Start celery beat:**
```bash
# /services/{service_name}
celery -A service beat --loglevel=info
```


## Databases

This module provides shared_tasks for working with databases.

### Methods

- `add_event(event: Event)` - adds event to the database.
- `get_event(event_id: int)` - gets event from the database.
- `get_events()` - gets all events from the database.
- `find_events(name: str, tag: str, type: str, later_than: datetime, earlier_than: datetime, limit: int, threshold: int)` - finds events by name, tag, type, time, limit and threshold(all parameters are optional).

- `update_event(event: Event)` - updates event in the database.
- `delete_event(event_id: int)` - deletes event from the database.
- `subscribe(user_id: int, tag: str)` - subscribes user to the event by tag.
- `unsubscribe(user_id: int, tag: str)` - unsubscribes user from the event by tag.
- `subscribers(tag: str)` - gets all subscribers by tag.

### Usage

```python
from common_utils import IDatabase

events = IDatabase.get_events.apply_async().get()
future_events = IDatabase.find_events.apply_async(kwargs={
    "later_than": datetime.now(),
    "limit": 10
}).get()
```

