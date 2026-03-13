# backend/app/main.py
import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Импортируем из наших модулей
from .database import engine, get_db, SessionLocal
from .models import Base, User

from .auth.router import router as auth_router

# Создаем таблицы
Base.metadata.create_all(bind=engine)

app = FastAPI(title="ALT+F4 backend")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(auth_router, prefix="/api/v1")


@app.get("/")
def root(db: Session = Depends(get_db)):
    """
    Возвращает статус backend
    """
    return {"message": "Hello from FastAPI backend!"}


@app.get("/users", response_model=dict)
def get_all_users(db: Session = Depends(get_db)):
    """
    Возвращает всех пользователей
    """
    try:
        users = db.query(User).all()
        users_list = [
            {
                "email": user.email,
                "full_name": user.full_name,
                "is_active": bool(user.is_active)
            }
            for user in users
        ]
        return {
            "count": len(users_list),
            "users": users_list
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка базы данных: {str(e)}")


@app.get("/users/{email}", response_model=dict)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    """
    Возвращает конкретного пользователя по email
    """
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(
                status_code=404, 
                detail=f"Пользователь с email {email} не найден"
            )
        return {
            "email": user.email,
            "full_name": user.full_name,
            "is_active": bool(user.is_active)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка базы данных: {str(e)}")
        
 # Защищенный эндпоинт для примера
@app.get("/api/v1/users")
def get_users():
    # Здесь будет логика получения пользователей
    return {"users": []}
           


'''
import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Импортируем из наших модулей
from .database import engine, get_db, SessionLocal
from .models import Base, User

app = FastAPI(title="ALT+F4 backend")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root(db: Session = Depends(get_db)):
    """
    Возвращает статус backend
    """
    return {"message": "Hello from FastAPI backend!"}


@app.get("/users", response_model=dict)
def get_all_users(db: Session = Depends(get_db)):
    """
    Возвращает всех пользователей
    """
    try:
        users = db.query(User).all()
        users_list = [
            {
                "email": user.email,
                "full_name": user.full_name,
                "is_active": bool(user.is_active)
            }
            for user in users
        ]
        return {
            "count": len(users_list),
            "users": users_list
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка базы данных: {str(e)}")


@app.get("/users/{email}", response_model=dict)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    """
    Возвращает конкретного пользователя по email
    """
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(
                status_code=404, 
                detail=f"Пользователь с email {email} не найден"
            )
        return {
            "email": user.email,
            "full_name": user.full_name,
            "is_active": bool(user.is_active)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка базы данных: {str(e)}")
'''












