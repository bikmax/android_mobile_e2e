import time
from collections import defaultdict
from reporting.TelegramReport import TelegramReport
from core.api.AuthController import AuthController
from core.data.test_data import TestData


class ResultCollector:
    _instance = None
    results = []
    start_time = time.time()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def add_result(self, name: str, status: str, report_url: str, duration: float, bug_link: str = None) -> None:
        """Добавляет результат теста, избегая дублирования"""
        if any(r['name'] == name and r['url'] == report_url for r in self.results):
            return  # Пропустить добавление дублирующегося результата

        result = {
            "name": name,
            "status": status,
            "url": report_url,
            "duration": duration
        }
        if bug_link:
            result["bug_link"] = bug_link

        self.results.append(result)

    def generate_report(self) -> list[str]:
        """Генерирует итоговый отчет, разбитый на части по 4096 символов"""
        successful = sum(1 for r in self.results if r["status"] == "🟢")
        failed = sum(1 for r in self.results if r["status"] == "🔴")
        skipped = sum(1 for r in self.results if r["status"] == "🟡")
        total = len(self.results)
        success_rate = (successful / total) * 100 if total > 0 else 0
        total_duration = sum(r["duration"] for r in self.results)

        # Форматируем список тестов
        test_lines = [
            f"{i}. {r['status']} {self._format_test_name(r)} {self._format_report_link(r['url'])}"
            for i, r in enumerate(self.results, 1)
        ]

        # Заголовок и статистика
        header = [
            "Итоговый отчёт",
            "",
        ]
        footer = [
            "",
            "Статистика",
            f"✅ Успешно: {successful} | ❌ Упало: {failed} | Пропущено: {skipped}",
            f"💹 Успешность: {success_rate:.1f}%",
            f"⏱️ Общее время выполнения: {self._format_duration(total_duration)}",
            f"🌀 Всего тестов: {total}"
        ]

        # Собираем весь текст
        full_report = header + test_lines + footer
        text = "\n".join(full_report)

        auth_controller = AuthController()
        auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend2)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend3)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend4)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend5)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend6)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend7)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend8)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend_alive)

        auth_controller.authenticate_and_delete_user(TestData.phone_prod_friend1)
        auth_controller.authenticate_and_delete_user(TestData.phone_prod_friend2)
        auth_controller.authenticate_and_delete_user(TestData.phone_prod_friend3)
        auth_controller.authenticate_and_delete_user(TestData.phone_prod_friend4)
        auth_controller.authenticate_and_delete_user(TestData.phone_prod_friend5)
        auth_controller.authenticate_and_delete_user(TestData.phone_prod_friend6)
        auth_controller.authenticate_and_delete_user(TestData.phone_prod_friend7)
        auth_controller.authenticate_and_delete_user(TestData.phone_prod_friend8)
        auth_controller.authenticate_and_delete_user(TestData.phone_prod_friend9)

        # Разбиваем на части по 4096 символов
        chunks = []
        current_chunk = ""
        for line in full_report:
            if len(current_chunk) + len(line) + 1 > 4096:
                chunks.append(current_chunk)
                current_chunk = line
            else:
                current_chunk += ("\n" if current_chunk else "") + line

        if current_chunk:
            chunks.append(current_chunk)

        return chunks

    def _format_test_name(self, result: dict) -> str:
        """Форматирует название теста с учетом bug_link для статуса 🟡"""
        name = result["name"]
        if result["status"] == "🟡" and "bug_link" in result and result["bug_link"]:
            return TelegramReport.format_link(name, result["bug_link"])
        return name

    def _format_report_link(self, url: str) -> str:
        """Форматирует ссылку на отчет"""
        if url.startswith(("http://", "https://")):
            return TelegramReport.format_link("Отчёт", url)
        return ""

    def _format_duration(self, seconds: float) -> str:
        """Форматирует время выполнения"""
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins}:{secs}" if mins else f"{secs}s"