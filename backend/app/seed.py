import os
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from database import engine, get_db, SessionLocal
from models import Base, User

# Тестовые данные
SAMPLE_USERS = [
    {"email": "user1@example.com", "full_name": "Иван Петров", "is_active": 1},
    {"email": "user2@example.com", "full_name": "Мария Сидорова", "is_active": 1},
    {"email": "user3@example.com", "full_name": "Алексей Иванов", "is_active": 0},
]

def init_database():
    """Инициализирует базу данных и создаёт таблицы"""
    # Создаём все таблицы (используем глобальный engine из database.py)
    Base.metadata.create_all(bind=engine)
    print("✅ Таблицы созданы")
    db = SessionLocal()
    try:
        user_count = db.query(User).count()
        if user_count == 0:
            users = [User(**user_data) for user_data in SAMPLE_USERS]
            db.add_all(users)  # Добавляем всех пользователей
            db.commit()
            print(f"✅ Добавлено пользователей: {len(SAMPLE_USERS)}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        db.rollback()
    finally:
        db.close()
    return engine
    
def main():
    engine = init_database()

if __name__ == "__main__":
    main()
    
    
'''
import sqlite3
from datetime import datetime
import os

# Тестовые данные
SAMPLE_USERS = [
	("user1@example.com", "Иван Петров", 1),
	("user2@example.com", "Мария Сидорова", 1),
	("user3@example.com", "Алексей Иванов", 0)
]

CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
	email TEXT,
	full_name TEXT,
	is_active INTEGER
);
"""


def init_database(db_path):
	# Просто открываем соединение - SQLite создаст файл
	conn = sqlite3.connect(db_path)    
	cursor = conn.cursor()
	cursor.execute(CREATE_USERS_TABLE)
	conn.commit()    
       
	cursor.execute("SELECT COUNT(*) FROM users")
	users_count = cursor.fetchone()[0]
	if users_count == 0:
		cursor.executemany("INSERT INTO users (email, full_name, is_active) VALUES (?, ?, ?)", SAMPLE_USERS)
	conn.commit()
    
	conn.close()
	return True
    

def main():
	init_database("ALT_F4.db")
    
if __name__ == "__main__":
	main()
'''