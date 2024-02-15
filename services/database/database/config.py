from turtle import pos
from common_utils.config import ConfigLoader, ConfigNode

loader = ConfigLoader(config_file="database")

class DatabaseConfig:
    class Mongo:
        username = loader.Field("mongo.username", env="MONGO_USER")
        password = loader.Field("mongo.password", env="MONGO_PASSWORD")
        port = loader.Field("mongo.port", env="MONGO_PORT")
        host = loader.Field("mongo.host", env="MONGO_HOST")
        db = loader.Field("mongo.db", env="MONGO_DB")
        
    class Postgres:
        username = loader.Field("postgres.username", env="POSTGRES_USER")
        password = loader.Field("postgres.password", env="POSTGRES_PASSWORD")
        port = loader.Field("postgres.port", env="POSTGRES_PORT")
        host = loader.Field("postgres.host", env="POSTGRES_HOST")
        db = loader.Field("postgres.db", env="POSTGRES_DB")
        
    postgres = loader.Field("postgres")
    mongo = loader.Field("mongo")
