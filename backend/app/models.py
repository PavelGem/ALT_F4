from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Создаём базовый класс для моделей
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'   
    email = Column(String, primary_key=True)
    full_name = Column(String)
    is_active = Column(Integer, default=1)    
    def __repr__(self):
        return f"<User(email='{self.email}')>"
