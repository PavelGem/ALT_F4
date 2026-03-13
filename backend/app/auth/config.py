
# backend/app/auth/config.py
from pydantic_settings import BaseSettings
from typing import List
import secrets

class AuthSettings(BaseSettings):
    # JWT настройки
    SECRET_KEY: str = secrets.token_urlsafe(32)  # В продакшене через .env!
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Настройки безопасности
    BCRYPT_ROUNDS: int = 12
    TOKEN_AUDIENCE: str = "alt-f4-client"
    TOKEN_ISSUER: str = "alt-f4-backend"
    
    class Config:
        env_file = ".env"
        env_prefix = "AUTH_"

auth_settings = AuthSettings()