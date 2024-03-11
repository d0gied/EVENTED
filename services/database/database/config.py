from pydantic import Field, MongoDsn, PostgresDsn
from pydantic_settings import BaseSettings


class DatabaseConfig(BaseSettings):
    mongo_dns: MongoDsn = Field(validation_alias="MONGO_URL")
    pg_dns: PostgresDsn = Field(validation_alias="PG_URL")

    celery_broker: str = Field(validation_alias="CELERY_BROKER_URL")
    celery_backend: str = Field(validation_alias="CELERY_RESULT_BACKEND")

    class Config:
        extra = "ignore"
        ...
