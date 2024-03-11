from pydantic import Field
from pydantic_settings import BaseSettings


class CeleryConfig(BaseSettings):
    celery_broker: str = Field(validation_alias="CELERY_BROKER_URL")
    celery_backend: str = Field(validation_alias="CELERY_RESULT_BACKEND")

    class Config:
        extra = "ignore"
