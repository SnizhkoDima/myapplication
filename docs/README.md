# MyApplication

Графічний додаток для підготовки до екзаменаційних тестів. Використовує PyQt5, SQLite та об'єктно-орієнтовану структуру.

---

## 🚀 Запуск

```bash
python main.py
```

---

## 🧾 Документування коду

У цьому проєкті використовується **Sphinx** для автоматичної генерації документації з Python-коду.

### 📌 Стиль оформлення

Використовується **reStructuredText (reST)** у docstring-коментарях.

#### Приклад:

```python
def fetch_data(filename):
    """
    Завантажує дані з JSON-файлу.

    :param filename: Шлях до файлу
    :type filename: str
    :return: Дані з файлу
    :rtype: dict
    """
```

### 📋 Правила:

- Документуйте **всі публічні функції, класи та методи**
- Коментарі пишуться **українською мовою**
- Структура docstring має відповідати **PEP 257** + **reST**
- Зміни інтерфейсу потребують оновлення документації

---

## 🛠 Генерація документації

Ми використовуємо `Sphinx`:
- Вихідна документація міститься у папці `docs/`
- Інструкція для генерації: [`docs/generate_docs.md`](docs/generate_docs.md)

---

## 📂 Структура проєкту

```
main.py
login_dialog.py
screens.py
widgets.py
models.py
database.py
data_loader.py
data/
docs/
README.md
```