from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Library API"
    debug: bool = False
    seed_data: bool = True
    database_url: str = "postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/library"

    model_config = SettingsConfigDict(env_file=".env")   # leave whatever you already have here

settings = Settings()