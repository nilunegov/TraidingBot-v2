import logging
import os

LOG_PATH = os.getenv("LOG_PATH", "../logs.log")
LOG_TO_CONSOLE = os.getenv("LOG_TO_CONSOLE", False)
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Создаем папку для логов, если её нет
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

def get_logger(name="trading-bot"):
    numeric_level = getattr(logging, LOG_LEVEL, logging.INFO)
    logging.basicConfig(
        filename=LOG_PATH,  # Файл, куда записываются логи
        level=numeric_level,  # Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Создаем логгер
    logger = logging.getLogger(name)

    # Если LOG_TO_CONSOLE = True, то добавляем вывод в консоль
    if LOG_TO_CONSOLE:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(numeric_level)
        console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        logger.addHandler(console_handler)

    return logger