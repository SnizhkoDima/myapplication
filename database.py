# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Назва файлу бази даних
DB_NAME = 'exam_preparation.db'

# Створення "двигуна" для підключення до SQLite
# 'echo=False' означає, що SQL-запити не будуть виводитись у консоль
engine = create_engine(f'sqlite:///{DB_NAME}', echo=False)

# Створення фабрики сесій для взаємодії з БД
Session = sessionmaker(bind=engine)