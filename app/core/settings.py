from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str
    ENV: str
    DB_URL: str
    OPEN_API_KEY: str
    GMAIL_USERNAME: str
    GMAIL_PASSWORD: str
    GMAIL_IMAP_URL: str
    GMAIL_IMAP_PORT: int
    ATTACHMENT_DIR: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


# Create a singleton instance of Settings
settings = Settings()



