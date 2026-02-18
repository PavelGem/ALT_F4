import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
#from typing import List

# Импортируем из наших модулей
from .database import engine, get_db, SessionLocal
from .models import Base, User

# Создаём таблицы (при необходимости)
# Base.metadata.create_all(bind=engine)

app = FastAPI(title="Моё приложение")

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
import sqlite3
import functions
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict

DATABASE_PATH = "test.db"

app = FastAPI(title="Мое приложение")

# Настройка CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ # Адреса фронтенда
        "http://localhost:3000",  
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn
 
@app.get("/")
def root():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT email FROM users")
        rows = cursor.fetchall()
        conn.close()
        emails = [row["email"] for row in rows]
        if not emails:
            return {"message": "База данных пуста"}
        return {"message": ", ".join(emails)}
    except Exception as e:
    	return {"message": {str(e)}}
'''



