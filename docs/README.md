# MyApplication

Цей проєкт є системою тестування з навчальними матеріалами. Він розроблений з використанням Python, FastAPI, SQLAlchemy та SQLite.

## 📦 Основні компоненти

- **FastAPI** — бекенд-фреймворк
- **SQLite** — СУБД для зберігання питань, результатів, користувачів
- **SQLAlchemy** — ORM для роботи з БД
- **Sphinx** — інструмент генерації документації

## 🚀 Інструкція для розробника

### 1. Клонування репозиторію

```bash
git clone https://github.com/SnizhkoDima/myapplication.git
cd myapplication
```

### 2. Встановлення Python

Встановіть Python версії **3.11** з офіційного сайту: https://www.python.org/downloads/

> Перевірити встановлення:
```bash
python --version
```

### 3. Створення віртуального середовища

```bash
python -m venv .venv
```

> Для Windows:
```bash
.venv\Scripts\activate
```
> Для Linux/macOS:
```bash
source .venv/bin/activate
```

### 4. Встановлення залежностей

```bash
pip install -r requirements.txt
```

### 5. Ініціалізація бази даних

```bash
python models.py
```

Цей крок створить всі необхідні таблиці в `SQLite` БД.

### 6. Запуск застосунку у режимі розробки

```bash
uvicorn main:app --reload
```

Після запуску відкрийте у браузері:
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## 🛠 Основні команди

| Команда | Опис |
|--------|------|
| `python models.py` | Ініціалізує структуру БД |
| `uvicorn main:app --reload` | Запускає API |
| `sphinx-build -b html docs/source docs/build` | Генерує документацію (за наявності) |

## 📚 Документація

Документація проєкту створюється за допомогою **Sphinx** і доступна в директорії `docs/`.

### Генерація документації:

```bash
cd docs
sphinx-build -b html source build
```

## 🔗 Корисні посилання

- [FastAPI](https://fastapi.tiangolo.com/)
- [Sphinx](https://www.sphinx-doc.org/)
- [GitHub репозиторій](https://github.com/SnizhkoDima/myapplication)