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