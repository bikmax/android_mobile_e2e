import os
import sys
import signal
import threading
import requests
import pytest

# === Глобальная переменная для хранения session_id'ов Sauce Labs ===
sauce_session_ids = []

# === Обработка сигнала завершения пайплайна ===
def terminate_all_sauce_sessions():
    SAUCE_USERNAME = os.environ.get("SAUCE_USERNAME")
    SAUCE_ACCESS_KEY = os.environ.get("SAUCE_ACCESS_KEY")

    if not SAUCE_USERNAME or not SAUCE_ACCESS_KEY:
        print("⚠️ No Sauce Labs credentials found. Skipping session termination.")
        return

    if not sauce_session_ids:
        print("⚠️ No Sauce Labs session IDs found to terminate.")
        return

    for session_id in sauce_session_ids:
        if not session_id.strip():
            continue
        url = f"https://api.us-west-1.saucelabs.com/rest/v1/{SAUCE_USERNAME}/jobs/{session_id}/stop"
        try:
            response = requests.put(url, auth=(SAUCE_USERNAME, SAUCE_ACCESS_KEY))
            print(f"🛑 Terminating session {session_id} -> Status: {response.status_code}")
        except Exception as e:
            print(f"❌ Failed to terminate session {session_id}: {e}")

def handle_termination(signum, frame):
    print(f"⚠️ Received termination signal ({signum}). Cleaning up Sauce Labs sessions...")
    terminate_all_sauce_sessions()
    sys.exit(0)

# === Основной запуск тестов ===
def run_tests(platform=None, marker=None, filename=None):
    """
    Пример запуска:
    python tests/runner.py --platform android --marker "regress" --filename app-rc-v.1.9.4-b639cac5.apk
    """
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sys.path.insert(0, root_dir)

    if platform:
        os.environ["TEST_PLATFORM"] = platform.lower()

    if filename:
        os.environ["TEST_APP_FILENAME"] = filename

    # Если есть ENV-переменная с session_id'ами, заполняем список
    session_ids_raw = os.environ.get("SAUCE_SESSION_IDS", "")
    for sid in session_ids_raw.split(","):
        if sid.strip():
            sauce_session_ids.append(sid.strip())

    # Запускаем pytest
    pytest_args = ["tests/"]
    if marker:
        pytest_args.append(f"-m {marker}")

    # Запуск с кодом возврата
    exit_code = pytest.main(pytest_args)
    sys.exit(exit_code)

# === Входная точка ===
if __name__ == "__main__":
    # Регистрируем обработчики сигналов SIGTERM и SIGINT
    signal.signal(signal.SIGTERM, handle_termination)
    signal.signal(signal.SIGINT, handle_termination)

    platform = None
    marker = None
    filename = None

    # Разбор аргументов
    if "--platform" in sys.argv:
        idx = sys.argv.index("--platform") + 1
        if idx < len(sys.argv):
            platform = sys.argv[idx]

    if "--marker" in sys.argv:
        idx = sys.argv.index("--marker") + 1
        if idx < len(sys.argv):
            marker = sys.argv[idx]

    if "--filename" in sys.argv:
        idx = sys.argv.index("--filename") + 1
        if idx < len(sys.argv):
            filename = sys.argv[idx]

    run_tests(platform, marker, filename)
