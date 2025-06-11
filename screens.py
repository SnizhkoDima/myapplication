"""
Модуль, що містить різні екрани інтерфейсу користувача для додатку.
"""
import random
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox,
                               QTextBrowser, QButtonGroup, QRadioButton, QMessageBox)
from PySide6.QtCore import Qt
from sqlalchemy.orm import joinedload

from database import Session
from models import Question, Result, Material
# Імпортуємо StatsCanvas з нового місця
from widgets import StatsCanvas


class HomeScreen(QWidget):
    """
    Екран привітання, що дозволяє користувачеві вибрати тему тесту.
    """
    def __init__(self, user, main_window):
        """
        Ініціалізує HomeScreen.
        """
        super().__init__()
        self.user = user
        self.main_window = main_window

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        welcome_label = QLabel(f"<h1>Вітаємо, {self.user.username}!</h1>")
        welcome_label.setAlignment(Qt.AlignCenter)

        info_label = QLabel("Оберіть галузь права, щоб розпочати підготовку.")
        info_label.setAlignment(Qt.AlignCenter)

        self.topic_combo = QComboBox()
        with Session() as session:
            topics = [q.topic for q in session.query(Question.topic).distinct().all()]
            self.topic_combo.addItems(topics)

        start_btn = QPushButton("Почати тест")
        start_btn.clicked.connect(self.start_test)

        layout.addWidget(welcome_label)
        layout.addWidget(info_label)
        layout.addWidget(self.topic_combo)
        layout.addWidget(start_btn)
        layout.addStretch()

    def start_test(self):
        """
        Розпочинає новий тест на основі обраної теми.
        """
        selected_topic = self.topic_combo.currentText()
        self.main_window.start_test_by_topic(selected_topic)


class MaterialsScreen(QWidget):
    """
    Екран для перегляду навчальних матеріалів за темами.
    """
    def __init__(self, main_window):
        """
        Ініціалізує MaterialsScreen.
        """
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout(self)
        self.topic_combo = QComboBox()
        self.material_browser = QTextBrowser()

        with Session() as session:
            topics = [m.topic for m in session.query(Material.topic).distinct().all()]
            self.topic_combo.addItems(topics)

        self.topic_combo.currentTextChanged.connect(self.load_material)

        layout.addWidget(QLabel("<h3>Оберіть тему для перегляду матеріалів:</h3>"))
        layout.addWidget(self.topic_combo)
        layout.addWidget(self.material_browser)
        self.load_material(self.topic_combo.currentText())

    def load_material(self, topic_name):
        """
        Завантажує та відображає навчальний матеріал для обраної теми.
        """
        with Session() as session:
            material = session.query(Material).filter_by(topic=topic_name).first()
            if material:
                self.material_browser.setHtml(material.material_text)
            else:
                self.material_browser.setHtml("<i>Матеріали для цієї теми відсутні.</i>")


class TestScreen(QWidget):
    """
    Екран для проходження тесту.
    """
    def __init__(self, user, topic, main_window):
        """
        Ініціалізує TestScreen.
        """
        super().__init__()
        self.user = user
        self.topic = topic
        self.main_window = main_window

        self.layout = QVBoxLayout(self)
        self.question_label = QLabel()
        self.question_label.setWordWrap(True)
        self.options_layout = QVBoxLayout()
        self.radio_group = QButtonGroup()

        self.next_btn = QPushButton("Наступне питання")
        self.next_btn.clicked.connect(self.process_next_question)

        self.layout.addWidget(self.question_label)
        self.layout.addLayout(self.options_layout)
        self.layout.addStretch()
        self.layout.addWidget(self.next_btn)

        self.load_questions()
        self.display_question()

    def load_questions(self):
        """
        Завантажує питання для тесту з бази даних і перемішує їх.
        """
        with Session() as session:
            self.questions = session.query(Question).filter_by(topic=self.topic).options(
                joinedload(Question.options)).all()
            random.shuffle(self.questions)
        self.current_question_index = 0
        self.correct_answers_count = 0

    def display_question(self):
        """
        Відображає поточне питання та варіанти відповідей.
        """
        for i in reversed(range(self.options_layout.count())):
            self.options_layout.itemAt(i).widget().setParent(None)

        q_data = self.questions[self.current_question_index]
        self.question_label.setText(
            f"<h3>Питання {self.current_question_index + 1}/{len(self.questions)}:</h3><p>{q_data.question_text}</p>")

        self.radio_group = QButtonGroup()
        for option in q_data.options:
            rb = QRadioButton(option.option_text)
            self.radio_group.addButton(rb, option.id)
            self.options_layout.addWidget(rb)

        if self.current_question_index == len(self.questions) - 1:
            self.next_btn.setText("Завершити тест")

    def process_next_question(self):
        """
        Обробляє відповідь користувача на поточне питання та переходить до наступного.
        """
        checked_id = self.radio_group.checkedId()
        if checked_id == -1:
            QMessageBox.warning(self, "Увага", "Оберіть варіант відповіді.")
            return

        if checked_id == self.questions[self.current_question_index].correct_option_id:
            self.correct_answers_count += 1

        self.current_question_index += 1
        if self.current_question_index < len(self.questions):
            self.display_question()
        else:
            self.finish_test()

    def finish_test(self):
        """
        Завершує тест, зберігає результати та повертається на головний екран.
        """
        total = len(self.questions)
        new_result = Result(user_name=self.user.username, topic=self.topic, score=self.correct_answers_count,
                            total_questions=total)
        with Session() as session:
            session.add(new_result)
            session.commit()

        percentage = (self.correct_answers_count / total * 100) if total > 0 else 0
        QMessageBox.information(self, "Результат",
                                f"Тест завершено!\nПравильних відповідей: {self.correct_answers_count} з {total} ({percentage:.2f}%)")
        self.main_window.show_main_screen(remove_test_screen=self)


class ResultsScreen(QWidget):
    """
    Екран для відображення статистики результатів тестів користувача.
    """
    def __init__(self, user, main_window):
        """
        Ініціалізує ResultsScreen.
        """
        super().__init__()
        self.user = user
        self.main_window = main_window
        layout = QVBoxLayout(self)
        self.stats_canvas = StatsCanvas(self)
        layout.addWidget(self.stats_canvas)
        self.load_results()

    def load_results(self):
        """
        Завантажує останні результати тестів користувача та відображає їх у вигляді графіка.
        """
        with Session() as session:
            results = session.query(Result).filter_by(user_name=self.user.username).order_by(
                Result.date_passed.desc()).all()

        if not results:
            self.stats_canvas.axes.clear()
            self.stats_canvas.axes.text(0.5, 0.5, 'Дані відсутні', horizontalalignment='center',
                                        verticalalignment='center')
            self.stats_canvas.draw()
            return

        latest_results = results[:10]
        latest_results.reverse()

        topics_dates = [f"{res.topic}\n{res.date_passed.strftime('%d.%m')}" for res in latest_results]
        percentages = [(res.score / res.total_questions * 100) for res in latest_results]

        self.stats_canvas.axes.clear()
        bars = self.stats_canvas.axes.bar(topics_dates, percentages)
        self.stats_canvas.axes.set_title(f'Останні 10 спроб для {self.user.username}')
        self.stats_canvas.axes.set_ylabel('Успішність, %')
        self.stats_canvas.axes.set_ylim(0, 105)
        self.stats_canvas.axes.tick_params(axis='x', rotation=45, labelsize=8)
        self.stats_canvas.axes.bar_label(bars, fmt='%.0f%%')
        self.stats_canvas.figure.tight_layout()
        self.stats_canvas.draw()