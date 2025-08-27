import pytest
import logging
from reporting.TelegramReport import TelegramReport
from ResultCollector import ResultCollector

logger = logging.getLogger(__name__)

def pytest_sessionfinish(session, exitstatus):
    """Отправка финального отчета в Telegram после завершения всех тестов"""
    report_chunks = ResultCollector().generate_report()

    for i, chunk in enumerate(report_chunks):
        print(f"\n[Часть {i+1}/{len(report_chunks)}]:\n{chunk}\n")
        if TelegramReport.send_tg(chunk):
            logger.info(f"Часть {i+1} отчета отправлена в Telegram")
        else:
            logger.warning(f"Не удалось отправить часть {i+1} отчета в Telegram")
