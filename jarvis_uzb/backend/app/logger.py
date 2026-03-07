import logging
from logging.handlers import RotatingFileHandler
import sys

def setup_logger():
    """
    Aylanma (rotating) fayl loggerini sozlaydi.
    Loglar ham faylga, ham konsolga yoziladi.
    """
    logger = logging.getLogger("jarvis_logger")
    logger.setLevel(logging.INFO)

    # Agar handlerlar allaqachon qo'shilgan bo'lsa, qayta qo'shmaslik
    if logger.hasHandlers():
        return logger

    # Faylga yozuvchi handler (1MB dan oshganda yangi fayl ochadi)
    file_handler = RotatingFileHandler('jarvis.log', maxBytes=1024*1024, backupCount=5, encoding='utf-8')
    
    # Konsolga yozuvchi handler
    console_handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

logger = setup_logger()