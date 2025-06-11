"""
Головний модуль програми для системи підготовки суддів.
Керує життєвим циклом додатку, включаючи вхід користувача та основне вікно.
"""
import os  # <-- Додаємо 'os' для сучасного налаштування High DPI
import sys

# QDialog тепер імпортується тут VVV
from PySide6.QtWidgets import QApplication, QDialog
# from PySide6.QtCore import QCoreApplication, Qt # Ці імпорти залишаються видаленими, оскільки вони не використовуються
from qt_material import apply_stylesheet

# Імпортуємо компоненти
from ui_main_window import ExamApp
from login_dialog import LoginDialog
from data_loader import seed_database
from models import create_db_tables


def main():
    """
    Основна функція для запуску додатку.
    """
    # Сучасний спосіб увімкнення High DPI (прибирає DeprecationWarning)
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"

    # Старі, застарілі рядки ми видалили.
    # QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    # QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    app.setProperty("logged_out", False)

    # Застосовуємо глобальну тему
    apply_stylesheet(app, theme='dark_teal.xml')

    # Створюємо таблиці в БД
    create_db_tables()
    # Заповнюємо даними (тільки якщо БД порожня)
    seed_database()

    while True:
        login_dialog = LoginDialog()
        # Тепер програма знає, що таке QDialog.Accepted VVV
        if login_dialog.exec() == QDialog.Accepted:
            current_user = login_dialog.get_user()

            main_window = ExamApp(user=current_user)
            main_window.show()

            app.exec()

            # Якщо користувач вийшов, цикл почнеться знову, показуючи вікно логіну
            if not app.property("logged_out"):
                break  # Вихід, якщо вікно було просто закрито
            else: # Видаляємо непотрібний else
                app.setProperty("logged_out", False)  # Скидаємо прапорець
        else:
            # Якщо користувач закрив вікно входу
            break

if __name__ == '__main__':
    main()
    # sys.exit() тут не потрібен, бо app.exec() керує виходом