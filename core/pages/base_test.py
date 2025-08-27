import os
import sys
import unittest
import time
import logging
import requests
import atexit
import signal

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from selenium.webdriver.support.ui import WebDriverWait
from ResultCollector import ResultCollector
from reporting.TelegramReport import TelegramReport
from core.api.AuthController import AuthController
from core.data.test_data import TestData

logger = logging.getLogger(__name__)

# === Глобальное хранилище текущей сессии (для аварийного завершения) ===
CURRENT_SESSION_ID = None


def emergency_terminate_session():
    """Аварийное завершение сессии Sauce Labs, если пайплайн был прерван"""
    global CURRENT_SESSION_ID
    session_id = CURRENT_SESSION_ID
    if not session_id:
        return

    username = os.getenv("SAUCE_USERNAME")
    access_key = os.getenv("SAUCE_ACCESS_KEY")
    if not username or not access_key:
        print("⚠️ No Sauce Labs credentials for emergency kill")
        return

    url = f"https://api.us-west-1.saucelabs.com/rest/v1/{username}/jobs/{session_id}/stop"
    try:
        resp = requests.put(url, auth=(username, access_key))
        print(f"⚠️ Emergency kill SauceLabs session {session_id}: HTTP {resp.status_code}")
    except Exception as e:
        print(f"❌ Failed to terminate session {session_id}: {e}")

# === Регистрируем хуки аварийного завершения ===
atexit.register(emergency_terminate_session)
signal.signal(signal.SIGTERM, lambda s, f: emergency_terminate_session())


class BaseTest(unittest.TestCase):
    SAUCE_URL = "https://ondemand.eu-central-1.saucelabs.com:443/wd/hub"
    result_collector = ResultCollector()

    def setUp(self):
        """Инициализация тестового окружения"""

        self._test_start_time = time.time()
        platform = os.getenv("TEST_PLATFORM", "android").lower()
        app_filename = os.getenv("TEST_APP_FILENAME", "app-prod.apk")
        #app_filename = os.getenv("TEST_APP_FILENAME")

        caps = self._get_capabilities(platform, app_filename)
        caps.set_capability("sauce:options", self._get_sauce_options(platform))

        self.driver = webdriver.Remote(self.SAUCE_URL, options=caps)
        self.wait = WebDriverWait(self.driver, 10)

        try:
            session_id = self.driver.session_id
            print(f"🆔 Sauce Labs session started: {session_id}")

            # Сохраняем в глобальную переменную для emergency_kill
            global CURRENT_SESSION_ID
            CURRENT_SESSION_ID = session_id

            # Также сохраняем в ENV (для runner.py)
            existing_ids = os.environ.get("SAUCE_SESSION_IDS", "")
            new_ids = f"{existing_ids},{session_id}" if existing_ids else session_id
            os.environ["SAUCE_SESSION_IDS"] = new_ids
        except Exception as e:
            print(f"⚠️ Could not obtain Sauce Labs session_id: {e}")

    def tearDown(self):
        """Завершение теста"""
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

        self._cleanup_driver()

    def _get_report_url(self) -> str:
        """Получает URL отчета из capabilities"""
        try:
            return self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        except:
            return "недоступен"

    def _send_failure_notification(self, error: str, report_url: str, duration: float) -> None:
        """Отправляет уведомление о падении теста"""
        message = (
            f"❌ <b>Test failed:</b> {self._get_test_name()}\n"
            f"🔥 <b>Error:</b> {error}\n"
            f"⏱ <b>Duration:</b> {ResultCollector()._format_duration(duration)}\n"
            f"🔗 {TelegramReport.format_link('Report', report_url)}"
        )
        TelegramReport.send_tg(message)

    def _cleanup_driver(self) -> None:
        """Корректно закрывает драйвер"""
        if hasattr(self, "driver") and self.driver:
            try:
                self.driver.quit()
            except:
                pass

    def _get_capabilities(self, platform: str, app_filename: str):
        """Возвращает capabilities для платформы"""
        if platform == "android":
            caps = UiAutomator2Options()
            caps.set_capability("platformName", "Android")
            caps.set_capability("appium:noReset", False)
            caps.set_capability("appium:fullReset", False)
            caps.set_capability("appium:appiumVersion", "2.0.0")
            caps.set_capability("appium:platformVersion", "15")
            caps.set_capability("appium:deviceName", "Google Pixel 9")
            caps.set_capability("appium:automationName", "UiAutomator2")
            caps.set_capability("appium:app", f"storage:filename={app_filename}")
            caps.set_capability("autoGrantPermissions", True)
        elif platform == "ios":
            caps = XCUITestOptions()
            caps.set_capability("platformName", "iOS")
            caps.set_capability("appium:platformVersion", "16")
            caps.set_capability("appium:deviceName", "iPhone.*")
            caps.set_capability("appium:automationName", "XCUITest")
            caps.set_capability("appium:app", f"storage:filename={app_filename}")
            caps.set_capability("autoAcceptAlerts", True)
        else:
            raise ValueError(f"Unsupported platform: {platform}")
        return caps

    def _get_sauce_options(self, platform: str) -> dict:
        """Возвращает опции для Sauce Labs"""
        return {
            "username": os.getenv("SAUCE_USERNAME", "uname"),
            "accessKey": os.getenv("SAUCE_ACCESS_KEY", "key"),
            "build": f"appium-build-{platform.upper()}",
            "name": f"{self.__class__.__name__}.{self._testMethodName}",
            "deviceOrientation": "PORTRAIT",
            "appiumVersion": "2.0.0"
        }
