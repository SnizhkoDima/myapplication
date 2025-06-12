# Інструкція з генерації документації

Цей проєкт використовує [Sphinx](https://www.sphinx-doc.org/) для автоматичної генерації документації з Python-коду.

## Кроки

1. Активуйте віртуальне середовище:
   ```bash
   source .venv/bin/activate  # або .venv\Scripts\activate на Windows
   ```

2. Встановіть залежності (один раз):
   ```bash
   pip install sphinx
   ```

3. Перейдіть у каталог `docs`:
   ```bash
   cd docs
   ```

4. Згенеруйте документацію:
   ```bash
   sphinx-build -b html source build
   ```

5. Відкрийте файл `docs/build/index.html` у браузері.

## Примітка

Нові Python-модулі слід додавати у файл `docs/source/modules.rst` у форматі:

```rst
.. automodule:: <назва_модуля>
   :members:
   :undoc-members:
   :show-inheritance:
```