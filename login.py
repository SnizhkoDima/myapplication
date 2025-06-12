import logging
logger = logging.getLogger(__name__)
...
def handle_login(self):
    ...
    if login_successful:
        logger.info(f"Успішний вхід користувача: {username}")
        ...
    else:
        logger.warning(f"Невдала спроба входу: {username}")
