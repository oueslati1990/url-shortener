from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://urluser:urlpass@localhost/urlshortener"
    short_code_length: int = 7
    base_url: str = "http://localhost:8000"
    allowed_origins: list[str] = ["http://localhost:4200"]

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
