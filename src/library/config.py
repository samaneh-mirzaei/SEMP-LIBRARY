from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Library API"
    debug: bool = False
    seed_data: bool = True

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()