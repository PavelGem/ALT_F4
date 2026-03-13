# backend/app/models.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, SmallInteger
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

#from .database import Base

# Создаём базовый класс для моделей
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Поля для безопасности
    last_login_ip = Column(String, nullable=True)
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    def __repr__(self):
        return f"<User(email='{self.email}')>"
    
    

'''
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Создаём базовый класс для моделей
Base = declarative_base()

# Создаем специально оформленный класс наследник от Base с описанием таблицы
# Класс Base сможет посмотреть всех своих наследников и создать таблицы вызвав Base.metadata.create_all(bind=engine)
class User(Base):
    __tablename__ = 'users'   
    email = Column(String, primary_key=True)
    full_name = Column(String)
    is_active = Column(Integer, default=1)    
    def __repr__(self):
        return f"<User(email='{self.email}')>"
'''