"""
Головний модуль програми для системи підготовки суддів.
Керує життєвим циклом додатку, включаючи вхід користувача та основне вікно.
"""

import os  # Додаємо 'os' для сучасного налаштування High DPI
import sys

from PySide6.QtWidgets import QApplication, QDialog
from qt_material import apply_stylesheet

from ui_main_window import ExamApp
from login_dialog import LoginDialog
from data_loader import seed_database
from models import create_db_tables


def main():
    """
    Основна функція для запуску додатку.

    Вона виконує:
    - Увімкнення підтримки High DPI
    - Ініціалізацію Qt-додатку з темою оформлення
    - Створення таблиць бази даних, якщо їх ще немає
    - Наповнення бази даних тестовими даними (один раз)
    - Цикл входу користувача та показу головного вікна

    Цикл повторюється, якщо користувач виходить із головного вікна через кнопку "Вийти".
    Усі інші способи завершують програму.
    """
    # Сучасний спосіб увімкнення High DPI (прибирає DeprecationWarning)
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"

    app = QApplication(sys.argv)
    app.setProperty("logged_out", False)

    # Застосовуємо глобальну тему оформлення
    apply_stylesheet(app, theme='dark_teal.xml')

    # Ініціалізуємо базу даних
    create_db_tables()
    seed_database()

    while True:
        login_dialog = LoginDialog()

        # Відображаємо діалог входу
        if login_dialog.exec() == QDialog.Accepted:
            current_user = login_dialog.get_user()

            main_window = ExamApp(user=current_user)
            main_window.show()

            app.exec()

            if not app.property("logged_out"):
                break  # Користувач закрив додаток
            else:
                app.setProperty("logged_out", False)  # Скидаємо прапорець для повторного входу
        else:
            break  # Користувач закрив вікно входу без авторизації


if __name__ == '__main__':
    main()
