import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ALT_F4.db")
# Чтобы разрешить многопоточность в SQLite, так как FastAPI многопоточный
if DATABASE_URL.startswith("sqlite"):
    DATABASE_URL += "?check_same_thread=False"
# Создаем движок и сессию SQLAlchemy (отключаем автокоммит и автофлеш) 
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Обертка для выдачи ви сессии, и ее авто завершения после выполнения запроса
def get_db():
    """Зависимость для получения сессии БД"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
