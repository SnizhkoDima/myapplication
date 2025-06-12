import logging

# Створення логера
logger = logging.getLogger("bosskfc")
logger.setLevel(logging.DEBUG)  # Базовий рівень — DEBUG (можна змінити через файл/змінну пізніше)

# Створення консолевого обробника
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Форматування
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
console_handler.setFormatter(formatter)

# Додавання обробника
logger.addHandler(console_handler)
