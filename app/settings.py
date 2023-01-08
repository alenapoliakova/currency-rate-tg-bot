from typing import Literal

from pydantic import BaseSettings, SecretStr, validator


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    SENDING_TYPE: Literal['webhook', 'polling'] = "polling"
    WEBHOOK_URL: str | None = None
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379

    @validator("WEBHOOK_URL", always=True)
    def check_sending_type(cls, value, values):
        if value is None and values["SENDING_TYPE"] == "webhook":
            raise ValueError("You need to set WEBHOOK_URL with SENDING_TYPE=<webhook>")
        return value

    class Config:
        env_file = '.env'


config = Settings()
