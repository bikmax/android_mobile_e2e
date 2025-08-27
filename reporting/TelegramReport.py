import requests
import time
import logging
from typing import Optional, Dict, Any
from urllib.parse import quote

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TelegramReport:
    # Конфигурация Telegram
    TG_TOKEN = "TG_TOKEN"
    TG_CHAT_ID = "TG_CHAT_ID"
    THREAD_ID = "THREAD_ID"
    API_TIMEOUT = 10  # seconds
    MAX_MESSAGE_LENGTH = 4096  # Telegram limit

    TG_TOKEN_alive_positive = "TG_TOKEN_alive_positive"
    TG_CHAT_ID_alive_positive = "TG_CHAT_ID_alive_positive"


    TG_TOKEN_alive_fail = "TG_TOKEN_alive_fail"
    TG_CHAT_ID_alive_fail = "TG_CHAT_ID_alive_fail"



    @classmethod
    def send_tg(
            cls,
            message: str,
            parse_mode: str = 'HTML',
            max_retries: int = 3,
            disable_notification: bool = False
    ) -> bool:
        """Улучшенная отправка сообщений в Telegram"""
        if not message or not isinstance(message, str):
            logger.error("Пустое или некорректное сообщение")
            return False

        # Обрезаем сообщение, если оно превышает лимит
        message = message[:cls.MAX_MESSAGE_LENGTH]

        url = f"https://api.telegram.org/bot{cls.TG_TOKEN}/sendMessage"
        payload = {
            'chat_id': cls.TG_CHAT_ID,
            'text': message,
            'parse_mode': parse_mode,
            'message_thread_id': cls.THREAD_ID,
            'disable_web_page_preview': True,
            'disable_notification': disable_notification
        }

        for attempt in range(max_retries):
            try:
                response = requests.post(
                    url,
                    json=payload,
                    timeout=cls.API_TIMEOUT
                )
                response.raise_for_status()

                if response.json().get('ok', False):
                    logger.info(f"Сообщение отправлено в Telegram (попытка {attempt + 1})")
                    time.sleep(1)
                    return True

                logger.error(f"Ошибка Telegram API: {response.text}")

            except requests.exceptions.RequestException as e:
                logger.error(f"Ошибка соединения (попытка {attempt + 1}): {str(e)}")

            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff

        logger.error(f"Не удалось отправить сообщение после {max_retries} попыток")
        time.sleep(1)
        return False

    @classmethod
    def send_tg_alive_positive(
            cls,
            message: str,
            parse_mode: str = 'HTML',
            max_retries: int = 3,
            disable_notification: bool = False
    ) -> bool:
        """Улучшенная отправка сообщений в Telegram"""
        if not message or not isinstance(message, str):
            logger.error("Пустое или некорректное сообщение")
            return False

        # Обрезаем сообщение, если оно превышает лимит
        message = message[:cls.MAX_MESSAGE_LENGTH]

        url = f"https://api.telegram.org/bot{cls.TG_TOKEN_alive_positive}/sendMessage"
        payload = {
            'chat_id': cls.TG_CHAT_ID_alive_positive,
            'text': message,
            'parse_mode': parse_mode,
            #'message_thread_id': cls.THREAD_ID_alive_positive,
            'disable_web_page_preview': True,
            'disable_notification': disable_notification
        }

        for attempt in range(max_retries):
            try:
                response = requests.post(
                    url,
                    json=payload,
                    timeout=cls.API_TIMEOUT
                )
                response.raise_for_status()

                if response.json().get('ok', False):
                    logger.info(f"Сообщение отправлено в Telegram (попытка {attempt + 1})")
                    return True

                logger.error(f"Ошибка Telegram API: {response.text}")

            except requests.exceptions.RequestException as e:
                logger.error(f"Ошибка соединения (попытка {attempt + 1}): {str(e)}")

            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff

        logger.error(f"Не удалось отправить сообщение после {max_retries} попыток")
        return False

    @classmethod
    def send_tg_alive_fail(
            cls,
            message: str,
            parse_mode: str = 'HTML',
            max_retries: int = 3,
            disable_notification: bool = False
    ) -> bool:
        """Улучшенная отправка сообщений в Telegram"""
        if not message or not isinstance(message, str):
            logger.error("Пустое или некорректное сообщение")
            return False

        # Обрезаем сообщение, если оно превышает лимит
        message = message[:cls.MAX_MESSAGE_LENGTH]

        url = f"https://api.telegram.org/bot{cls.TG_TOKEN_alive_fail}/sendMessage"
        payload = {
            'chat_id': cls.TG_CHAT_ID_alive_fail,
            'text': message,
            'parse_mode': parse_mode,
            # 'message_thread_id': cls.THREAD_ID_alive_positive,
            'disable_web_page_preview': True,
            'disable_notification': disable_notification
        }

        for attempt in range(max_retries):
            try:
                response = requests.post(
                    url,
                    json=payload,
                    timeout=cls.API_TIMEOUT
                )
                response.raise_for_status()

                if response.json().get('ok', False):
                    logger.info(f"Сообщение отправлено в Telegram (попытка {attempt + 1})")
                    return True

                logger.error(f"Ошибка Telegram API: {response.text}")

            except requests.exceptions.RequestException as e:
                logger.error(f"Ошибка соединения (попытка {attempt + 1}): {str(e)}")

            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff

        logger.error(f"Не удалось отправить сообщение после {max_retries} попыток")
        return False

    @classmethod
    def format_link(cls, text: str, url: str) -> str:
        """Безопасное форматирование ссылки"""
        if not url or not isinstance(url, str):
            logger.warning("Некорректный URL для ссылки")
            return text

        try:
            # Кодируем URL и экранируем HTML
            encoded_url = quote(url, safe='/:?=&')
            escaped_text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            return f'<a href="{encoded_url}">{escaped_text}</a>'
        except Exception as e:
            logger.error(f"Ошибка форматирования ссылки: {e}")
            return text

    @classmethod
    def send_document(
            cls,
            file_path: str,
            caption: str = "",
            max_retries: int = 3
    ) -> bool:
        """Отправка файла в Telegram"""
        try:
            with open(file_path, 'rb') as file:
                url = f"https://api.telegram.org/bot{cls.TG_TOKEN}/sendDocument"
                files = {'document': file}
                data = {
                    'chat_id': cls.TG_CHAT_ID,
                    'message_thread_id': cls.THREAD_ID,
                    'caption': caption[:1024]  # Ограничение Telegram
                }

                for attempt in range(max_retries):
                    try:
                        response = requests.post(
                            url,
                            files=files,
                            data=data,
                            timeout=cls.API_TIMEOUT
                        )
                        if response.json().get('ok', False):
                            return True
                    except Exception as e:
                        logger.error(f"Ошибка отправки файла (попытка {attempt + 1}): {e}")
                        time.sleep(2 ** attempt)

                return False
        except Exception as e:
            logger.error(f"Ошибка открытия файла: {e}")
            return False