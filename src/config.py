from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL :str 

    model_config = SettingsConfigDict(
        env_file = ".env",
        extra="ignore"  # Ignore any extra fields not defined in the model above the base settings one
    )



Config = Settings()