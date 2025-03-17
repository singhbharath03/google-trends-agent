from pydantic import BaseModel
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    app_name: str = "FastAPI App"
    debug_mode: bool = False
    database_url: str = "sqlite:///./test.db"
    api_key: Optional[str] = None
    private_key: Optional[str] = None
    groq_api_key: Optional[str] = None
    serp_api_key: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Create settings instance
settings = Settings()


# Function to get settings
def get_settings():
    return settings
