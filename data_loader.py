# data_loader.py
import json
from database import Session
from models import Question, Option, Material, create_db_tables


def seed_database():
    # Створюємо таблиці перед заповненням
    create_db_tables()

    with Session() as session:
        # Перевірка, чи дані вже існують
        if session.query(Question).first() or session.query(Material).first():
            print("База даних вже містить дані. Заповнення пропущено.")
            return

        # Завантаження матеріалів
        try:
            with open('data/materials.json', 'r', encoding='utf-8') as f:
                materials_data = json.load(f)
                for item in materials_data:
                    material = Material(
                        topic=item['topic'],
                        material_text=item['material_text']
                    )
                    session.add(material)
            print("Матеріали успішно завантажено.")
        except FileNotFoundError:
            print("Файл 'materials.json' не знайдено.")

        # Завантаження питань
        try:
            with open('data/questions.json', 'r', encoding='utf-8') as f:
                questions_data = json.load(f)
                for item in questions_data:
                    new_question = Question(
                        topic=item['topic'],
                        question_text=item['question_text']
                    )

                    options = []
                    for i, opt_text in enumerate(item['options']):
                        option = Option(option_text=opt_text, question=new_question)
                        options.append(option)
                        if i == item['correct_option_index']:
                            # Зберігаємо ID правильної відповіді після того, як її буде додано до БД
                            session.flush()  # Потрібно для присвоєння ID до комміту
                            new_question.correct_option_id = option.id

                    session.add(new_question)
            print("Питання успішно завантажено.")
        except FileNotFoundError:
            print("Файл 'questions.json' не знайдено.")

        session.commit()
        print("Заповнення бази даних завершено.")