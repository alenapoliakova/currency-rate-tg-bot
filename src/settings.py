from pydantic import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str
    BOT_NAME: str
    LOG_FILE_PATH: str = "log_file"

    class Config:
        env_file = '.env'


config = Settings()
