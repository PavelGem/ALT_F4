
# backend/app/auth/utils.py
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple
import uuid
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status

from .config import auth_settings

# Контекст для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthUtils:
    """Утилиты для авторизации"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Хеширование пароля"""
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Проверка пароля"""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(user_id: int) -> str:
        """Создание access токена"""
        now = datetime.utcnow()
        payload = {
            "sub": str(user_id),
            "type": "access",
            "jti": str(uuid.uuid4()),
            "iat": now,
            "nbf": now,
            "exp": now + timedelta(minutes=auth_settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            "aud": auth_settings.TOKEN_AUDIENCE,
            "iss": auth_settings.TOKEN_ISSUER,
        }
        return jwt.encode(
            payload, 
            auth_settings.SECRET_KEY, 
            algorithm=auth_settings.ALGORITHM
        )

    @staticmethod
    def create_refresh_token(user_id: int) -> str:
        """Создание refresh токена"""
        now = datetime.utcnow()
        payload = {
            "sub": str(user_id),
            "type": "refresh",
            "jti": str(uuid.uuid4()),
            "iat": now,
            "nbf": now,
            "exp": now + timedelta(days=auth_settings.REFRESH_TOKEN_EXPIRE_DAYS),
            "aud": auth_settings.TOKEN_AUDIENCE,
            "iss": auth_settings.TOKEN_ISSUER,
        }
        return jwt.encode(
            payload, 
            auth_settings.SECRET_KEY, 
            algorithm=auth_settings.ALGORITHM
        )

    @staticmethod
    def create_token_pair(user_id: int) -> Dict[str, str]:
        """Создание пары токенов"""
        return {
            "access_token": AuthUtils.create_access_token(user_id),
            "refresh_token": AuthUtils.create_refresh_token(user_id),
            "token_type": "bearer"
        }

    @staticmethod
    def verify_token(token: str, token_type: str = "access") -> Optional[Dict[str, Any]]:
        """Проверка токена"""
        try:
            payload = jwt.decode(
                token,
                auth_settings.SECRET_KEY,
                algorithms=[auth_settings.ALGORITHM],
                audience=auth_settings.TOKEN_AUDIENCE,
                issuer=auth_settings.TOKEN_ISSUER,
                options={"require": ["exp", "aud", "iss"]}
            )
            
            # Проверяем тип токена
            if payload.get("type") != token_type:
                return None
                
            return payload
        except JWTError:
            return None