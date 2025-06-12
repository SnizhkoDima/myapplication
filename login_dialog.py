"""
Модуль, що містить діалогове вікно для входу та реєстрації користувачів.
"""
import traceback
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLineEdit, QPushButton,
                               QLabel, QMessageBox)
from PySide6.QtCore import Qt
from database import Session
from models import User
from logger_config import logger


class LoginDialog(QDialog):
    """
    Діалогове вікно для входу або реєстрації користувачів у системі.
    """
    def __init__(self, parent=None):
        """
        Ініціалізує LoginDialog.
        """
        super().__init__(parent)
        self.setWindowTitle("Вхід та Реєстрація")
        self.setMinimumWidth(300)
        self.user = None

        # Створення віджетів
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Ім'я користувача")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.message_label = QLabel("")
        self.message_label.setStyleSheet("color: #e74c3c;")
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setWordWrap(True)

        login_btn = QPushButton("Увійти")
        register_btn = QPushButton("Зареєструватися")

        login_btn.setStyleSheet("background-color: #1abc9c; color: white; font-weight: bold; padding: 8px;")
        register_btn.setStyleSheet("background-color: #3498db; color: white; font-weight: bold; padding: 8px;")

        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.addWidget(QLabel("<strong>Ім'я користувача:</strong>"))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel("<strong>Пароль:</strong>"))
        layout.addWidget(self.password_input)
        layout.addWidget(self.message_label)
        layout.addWidget(login_btn)
        layout.addWidget(register_btn)

        login_btn.clicked.connect(self.handle_login)
        register_btn.clicked.connect(self.handle_register)

    def handle_login(self):
        """
        Обробляє спробу входу користувача.
        """
        username = self.username_input.text()
        password = self.password_input.text()
        try:
            with Session() as session:
                user = session.query(User).filter_by(username=username).first()
                if user and user.check_password(password):
                    self.user = user
                    logger.info(f"Користувач '{username}' увійшов у систему.")
                    self.accept()
                else:
                    logger.warning(f"Спроба входу з неправильними даними: '{username}'")
                    self.message_label.setText("Неправильне ім'я користувача або пароль.")
        except Exception as e:
            logger.error("Помилка при вході користувача: %s", traceback.format_exc())
            QMessageBox.critical(self, "Помилка", f"Сталася помилка при вході: {str(e)}")

    def handle_register(self):
        """
        Обробляє спробу реєстрації нового користувача.
        """
        username = self.username_input.text()
        password = self.password_input.text()
        if not username or len(password) < 4:
            self.message_label.setText("Ім'я не може бути порожнім, а пароль має бути не менше 4 символів.")
            return

        try:
            with Session() as session:
                if session.query(User).filter_by(username=username).first():
                    self.message_label.setText("Користувач з таким іменем вже існує.")
                    return

                new_user = User(username=username)
                new_user.set_password(password)
                session.add(new_user)
                session.commit()
                logger.info(f"Зареєстровано нового користувача: '{username}'")
                QMessageBox.information(self, "Успіх",
                                        f"Користувач '{username}' успішно зареєстрований! Тепер ви можете увійти.")
                self.message_label.setText("")
        except Exception as e:
            logger.error("Помилка при реєстрації: %s", traceback.format_exc())
            QMessageBox.critical(self, "Помилка", f"Сталася помилка при реєстрації: {str(e)}")

    def get_user(self):
        """
        Повертає об'єкт користувача, який успішно увійшов.
        """
        return self.user
