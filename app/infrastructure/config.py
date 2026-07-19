from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    port: int = Field(8000, validation_alias="PORT")
    host: str = Field("0.0.0.0", validation_alias="HOST")
    log_level: str = Field("info", validation_alias="LOG_LEVEL")

    openai_api_key: str = Field("", validation_alias="OPENAI_API_KEY")

    default_provider: str = Field("openai", validation_alias="DEFAULT_PROVIDER")
    default_model: str = Field("gpt-4o", validation_alias="DEFAULT_MODEL")


settings = Settings()
