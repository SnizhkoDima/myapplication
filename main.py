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
    logger.debug(f"Конфігураційна директорія: {config_dir}")
    return os.path.join(config_dir, "user_config.json")


def save_user_to_config(user):
    config_path = get_user_config_path()
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump({'user': user}, f)
        logger.info("Користувач успішно збережений до конфігурації.")
    except Exception as e:
        logger.error(f"Не вдалося зберегти користувача: {e}")


def load_user_from_config():
    config_path = get_user_config_path()
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            logger.info("Користувача завантажено з конфігурації.")
            return data.get('user')
    except Exception as e:
        logger.warning(f"Не вдалося завантажити користувача: {e}")
        return None


def main():
    logger.info("Запуск додатку...")

    app = QApplication(sys.argv)

    user = load_user_from_config()
    if user is None:
        login_dialog = LoginDialog()
        if login_dialog.exec():
            user = login_dialog.get_user()
            save_user_to_config(user)
        else:
            logger.info("Користувач скасував вхід. Завершення програми.")
            sys.exit(0)

    try:
        window = ExamApp(user)
        window.show()
        logger.info("Основне вікно відображено.")
        exit_code = app.exec()
        logger.info("Завершення додатку з кодом %s", exit_code)
        sys.exit(exit_code)
    except Exception as e:
        logger.critical("Невідома помилка у додатку:", exc_info=True)
        traceback.print_exc()
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Помилка")
        msg.setText("Сталася неочікувана помилка.")
        msg.setDetailedText(str(e))
        msg.exec()
        sys.exit(1)


if __name__ == "__main__":
    main()
