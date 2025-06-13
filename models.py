"""
Модуль, що містить моделі даних для бази даних SQLAlchemy.
"""
import datetime
import bcrypt
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base
from database import engine


# Базовий клас для всіх моделей
Base = declarative_base()


class User(Base):
    """
    Модель користувача для зберігання облікових даних.
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

    def set_password(self, password):
        """
        Встановлює хешований пароль для користувача.
        """
        pw_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(pw_bytes, salt).decode('utf-8')

    def check_password(self, password):
        """
        Перевіряє наданий пароль з хешованим паролем користувача.
        """
        pw_bytes = password.encode('utf-8')
        hash_bytes = self.password_hash.encode('utf-8')
        try:
            return bcrypt.checkpw(pw_bytes, hash_bytes)
        except ValueError:
            return False


class Question(Base):
    """
    Модель питання тесту.
    """
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    topic = Column(String, nullable=False, index=True)
    question_text = Column(Text, nullable=False)
    options = relationship("Option", back_populates="question", cascade="all, delete-orphan")
    correct_option_id = Column(Integer)


class Option(Base):
    """
    Модель варіанта відповіді для питання.
    """
    __tablename__ = 'options'
    id = Column(Integer, primary_key=True)
    option_text = Column(Text, nullable=False)
    question_id = Column(Integer, ForeignKey('questions.id'), nullable=False)
    question = relationship("Question", back_populates="options")


class Result(Base):
    """
    Модель результатів тестування користувача.
    """
    __tablename__ = 'results'
    id = Column(Integer, primary_key=True)
    user_name = Column(String, nullable=False, index=True)
    topic = Column(String, nullable=False)
    score = Column(Integer, nullable=False)
    total_questions = Column(Integer, nullable=False)
    date_passed = Column(DateTime, default=datetime.datetime.utcnow)


class Material(Base):
    """
    Модель навчальних матеріалів.
    """
    __tablename__ = 'materials'
    id = Column(Integer, primary_key=True)
    topic = Column(String, unique=True, nullable=False)
    material_text = Column(Text, nullable=False)


def create_db_tables():
    """
    Створює всі таблиці бази даних, визначені моделями.
    """
    Base.metadata.create_all(engine)