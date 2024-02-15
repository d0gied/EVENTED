from database.config import DatabaseConfig

config = DatabaseConfig()
print(config.Mongo.host)
print(config.postgres)

