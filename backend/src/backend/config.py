from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Google credentials identify the application to Google's OAuth service.
    google_client_id: str
    google_client_secret: str

    # Used to sign the session cookie used during the OAuth flow.
    session_secret: str

    # Used to sign and verify JWT access tokens.
    jwt_secret: str

    # LLM provider API key
    cohere_api_key: str

    # Load development configuration from .env file
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
