#load important settings from the .env file

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "DVMS"
    environment: str = "development"

    database_url: str = "sqlite:///./dvms.db"

    secret_key: str
    encryption_key: str
    blind_index_pepper: str

    access_token_expire_minutes: int = 60
    algorithm: str = "HS256"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

settings = Settings()

