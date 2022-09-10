from pydantic import BaseSettings, AnyUrl


class Settings(BaseSettings):
    JOKES_BASE_URL: AnyUrl

    class Config:
        case_sensitive: bool = True
        env_file = '.env'


def get_settings():
    return Settings()
