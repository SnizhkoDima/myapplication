# ui_main_window.py
import sys
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QPushButton, QStackedWidget, QLabel, QFrame, QApplication)
from PySide6.QtCore import Qt, QSize
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import qtawesome as qta


# Клас для графіка
class StatsCanvas(FigureCanvas):
    def __init__(self, parent=None):
        fig = Figure(figsize=(5, 4), dpi=100, facecolor='#f7f7f7')
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
        self.setParent(parent)


# Імпортуємо класи екранів
from screens import HomeScreen, MaterialsScreen, TestScreen, ResultsScreen


class ExamApp(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.current_user = user
        self.setWindowTitle(f"Система Підготовки Суддів")
        self.setGeometry(100, 100, 1200, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        nav_panel = QFrame()
        nav_panel.setFixedWidth(220)
        nav_panel.setStyleSheet("background-color: #2c3e50; color: white;")
        nav_layout = QVBoxLayout(nav_panel)
        nav_layout.setAlignment(Qt.AlignTop)
        nav_layout.setContentsMargins(10, 20, 10, 20)
        nav_layout.setSpacing(15)

        self.pages_stack = QStackedWidget()
        main_layout.addWidget(nav_panel)
        main_layout.addWidget(self.pages_stack)

        self.nav_buttons = {}
        nav_items = [
            ("fa5s.home", "Головна", HomeScreen(self.current_user, self)),
            ("fa5s.book-open", "Матеріали", MaterialsScreen(self)),
            ("fa5s.chart-line", "Статистика", ResultsScreen(self.current_user, self)),
        ]

        for icon, name, page in nav_items:
            button = QPushButton(name)
            button.setIcon(qta.icon(icon, color='white', color_active='#1abc9c'))
            button.setIconSize(QSize(22, 22))
            button.setCheckable(True)
            button.setAutoExclusive(True)
            button.clicked.connect(lambda checked, p=page: self.pages_stack.setCurrentWidget(p))
            nav_layout.addWidget(button)
            self.pages_stack.addWidget(page)
            self.nav_buttons[name] = button

        nav_layout.addStretch()

        user_info_label = QLabel(f"Користувач:\n<b>{self.current_user.username}</b>")
        user_info_label.setAlignment(Qt.AlignCenter)
        user_info_label.setWordWrap(True)

        logout_button = QPushButton("Вийти")
        logout_button.setIcon(qta.icon("fa5s.sign-out-alt", color='white'))
        logout_button.clicked.connect(self.logout)

        nav_layout.addWidget(user_info_label)
        nav_layout.addWidget(logout_button)

        self.apply_styles()
        self.nav_buttons["Головна"].setChecked(True)
        self.pages_stack.setCurrentIndex(0)

    def apply_styles(self):
        style = """
            QPushButton {
                color: white; background-color: transparent; border: none;
                padding: 12px; text-align: left; font-size: 16px; border-radius: 5px;
            }
            QPushButton:hover { background-color: #34495e; }
            QPushButton:checked { background-color: #1abc9c; font-weight: bold; }
        """
        self.centralWidget().setStyleSheet(style)

    def start_test_by_topic(self, topic_name):
        test_screen = TestScreen(self.current_user, topic_name, self)
        self.pages_stack.addWidget(test_screen)
        self.pages_stack.setCurrentWidget(test_screen)
        for btn in self.nav_buttons.values():
            btn.setChecked(False)

    def show_main_screen(self, remove_test_screen=None):
        if remove_test_screen:
            self.pages_stack.removeWidget(remove_test_screen)

        for i in range(self.pages_stack.count()):
            if isinstance(self.pages_stack.widget(i), HomeScreen):
                self.pages_stack.setCurrentIndex(i)
                self.nav_buttons["Головна"].setChecked(True)
                break

    def logout(self):
        self.close()
        # Потрібен перезапуск додатку, що реалізовано в main.py
        QApplication.instance().setProperty("logged_out", True)