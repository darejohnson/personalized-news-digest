from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API Keys
    newsapi_key: str
    openai_api_key: str
    
    # Application Settings
    debug: bool = False
    log_level: str = "INFO"
    
    # NewsAPI Settings
    newsapi_base_url: str = "https://newsapi.org/v2"
    
    # OpenAI Settings
    openai_model: str = "gpt-3.5-turbo"
    #openai_model: str = "GPT-4o"
    max_tokens: int = 150
    
    class Config:
        env_file = ".env"

settings = Settings()
