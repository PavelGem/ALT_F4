# backend/app/auth/router.py
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from datetime import datetime

from ..database import get_db
from ..models import User
from . import schemas
from .utils import AuthUtils
from .dependencies import AuthDependencies

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=schemas.UserResponse)
def register(
    user_data: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    """Регистрация нового пользователя"""
    
    # Проверяем, существует ли пользователь
    existing_user = db.query(User).filter(
        User.email == user_data.email
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    # Создаем пользователя
    hashed_password = AuthUtils.hash_password(user_data.password)
    
    # Извлекаем username из email (часть до @)
    username = user_data.email.split('@')[0]
    
    db_user = User(
        email=user_data.email,
        username=username,
        full_name=user_data.full_name,
        hashed_password=hashed_password,
        is_active=True
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.post("/login", response_model=schemas.TokenResponse)
def login(
    login_data: schemas.UserLogin,
    request: Request,
    db: Session = Depends(get_db)
):
    """Вход в систему"""
    
    # Ищем пользователя по email или username
    user = db.query(User).filter(
        (User.email == login_data.username) | 
        (User.username == login_data.username)
    ).first()
    
    if not user or not AuthUtils.verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email/username or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is deactivated"
        )
    
    # Обновляем информацию о входе
    user.last_login_at = datetime.utcnow()
    user.last_login_ip = request.client.host
    db.commit()
    
    # Создаем токены
    return AuthUtils.create_token_pair(user.id)

@router.post("/refresh", response_model=schemas.TokenResponse)
def refresh_token(
    refresh_data: schemas.TokenRefresh,
    db: Session = Depends(get_db)
):
    """Обновление access токена"""
    
    # Верифицируем refresh токен
    payload = AuthUtils.verify_token(refresh_data.refresh_token, "refresh")
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    user_id = int(payload.get("sub"))
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    # Создаем новую пару токенов
    return AuthUtils.create_token_pair(user.id)

@router.get("/me", response_model=schemas.UserResponse)
def get_current_user(
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Получение информации о текущем пользователе"""
    return current_user
    
