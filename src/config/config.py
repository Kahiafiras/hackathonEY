"""Module to call All configs"""
from functools import lru_cache
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Class to call all configs"""
    API_key: str
    LLAMA_CLOUD_API:str
  
@lru_cache()
def get_settings():
    environment = os.getenv("ENVIRONMENT", "local")
    if environment == "local":
        return Settings(_env_file=".env", _env_file_encoding="utf-8")  # type: ignore
    elif environment == "production":
        return Settings()
    else:
        raise ValueError("Invalid environment")
