# Резервне копіювання

Цей документ описує як створити резервну копію застосунку `myapplication`.

## Що слід резервувати
- Каталог з кодом проєкту
- Віртуальне середовище (опціонально)
- Базу даних SQLite (`app.db` або подібну)
- Файли конфігурації (якщо є)

## Покрокова інструкція

1. Зупиніть застосунок (якщо це можливо):
```bash
pkill gunicorn
```

2. Скопіюйте проєкт:
```bash
cp -r /path/to/myapplication /backup/location/myapplication_backup_$(date +%F)
```

3. Скопіюйте файл бази даних:
```bash
cp /path/to/myapplication/app.db /backup/location/app_backup_$(date +%F).db
```

4. (Опціонально) Заархівуйте для зручності:
```bash
tar -czvf myapplication_backup_$(date +%F).tar.gz /backup/location/myapplication_backup_$(date +%F)
```

## Перевірка
- Переконайтесь, що файли скопійовані.
- Розпакуйте архів та перевірте цілісність.
