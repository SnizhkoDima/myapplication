import sys
import os
import json
import traceback
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QStandardPaths
from login_dialog import LoginDialog
from ui_main_window import ExamApp
from logger_config import logger


def get_user_config_path():
    config_dir = QStandardPaths.writableLocation(QStandardPaths.AppConfigLocation)
    os.makedirs(config_dir, exist_ok=True)
    return os.path.join(config_dir, "user_config.json")


def save_user_to_config(user):
    config_path = get_user_config_path()
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump({'user': user}, f)
        logger.debug("Користувач успішно збережений у файл конфігурації.")
    except Exception as e:
        logger.exception("Не вдалося зберегти користувача в конфігурацію.")
        show_error("Помилка збереження", str(e))


def load_user_from_config():
    config_path = get_user_config_path()
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('user')
    except FileNotFoundError:
        logger.warning("Файл конфігурації користувача не знайдено.")
        return None
    except Exception as e:
        logger.exception("Не вдалося завантажити користувача з конфігурації.")
        return None


def show_error(title, details):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setWindowTitle(title)
    msg.setText("Сталася помилка.")
    msg.setDetailedText(details)
    msg.exec()


def main():
    logger.info("Запуск додатку...")

    app = QApplication(sys.argv)

    user = load_user_from_config()
    if user is None:
        login_dialog = LoginDialog()
        if login_dialog.exec():
            user = login_dialog.get_user()
            if not user:
                logger.warning("Користувач не ввів ім'я.")
                show_error("Помилка входу", "Ім'я користувача не може бути порожнім.")
                sys.exit(1)
            save_user_to_config(user)
        else:
            logger.info("Користувач скасував вхід. Завершення програми.")
            sys.exit(0)

    try:
        window = ExamApp(user)
        window.show()
        exit_code = app.exec()
        logger.info("Завершення додатку з кодом %s", exit_code)
        sys.exit(exit_code)
    except Exception as e:
        logger.exception("Невідома помилка під час запуску додатку.")
        show_error("Невідома помилка", str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
