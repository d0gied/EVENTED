from math import e

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings


class TelegramConfig(BaseSettings):
    token: SecretStr = Field(validation_alias="TELEGRAM_BOT_TOKEN")

    class Config:
        extra = "ignore"
