
# backend/app/auth/dependencies.py
from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import Optional

from ..database import get_db
from ..models import User
from .utils import AuthUtils

class AuthDependencies:
    """Зависимости для авторизации"""
    
    @staticmethod
    async def get_current_user(
        request: Request,
        db: Session = Depends(get_db)
    ) -> User:
        """Получение текущего пользователя из токена"""
        # Получаем токен из заголовка
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated"
            )
        
        token = auth_header.replace("Bearer ", "")
        
        # Верифицируем токен
        payload = AuthUtils.verify_token(token, "access")
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )
        
        # Получаем пользователя
        user_id = int(payload.get("sub"))
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inactive user"
            )
        
        return user

    @staticmethod
    async def get_optional_user(
        request: Request,
        db: Session = Depends(get_db)
    ) -> Optional[User]:
        """Опциональное получение пользователя (для публичных эндпоинтов)"""
        try:
            return await AuthDependencies.get_current_user(request, db)
        except HTTPException:
            return None
