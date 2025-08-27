from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import os

from webdriver_manager.chrome import ChromeDriverManager


def delete_apk_sauce():
    chrome_options = Options()
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")  # Для Docker обязательно
    chrome_options.add_argument("--headless")  # Если нужен headless режим

    # Webdriver-manager скачает нужную версию драйвера
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)


    try:
        # 1. Go to Sauce Labs app management page
        driver.get("https://app.eu-central-1.saucelabs.com/app-management")
        time.sleep(5)
        # 2. Type LOGIN into the username field
        username_input = driver.find_element(By.CSS_SELECTOR, 'input[type="text"]')
        username_input.send_keys("e2e@e2e")
        time.sleep(1)
        # 3. Type PASSWORD into the password field
        password_input = driver.find_element(By.CSS_SELECTOR, 'input[type="password"]')
        password_input.send_keys("1323312asds")
        time.sleep(2)
        # 4. Click on the submit button
        submit_button = driver.find_element(By.CSS_SELECTOR, 'input[id="loginButton_0"]')
        submit_button.click()

        # Give some time for the page to load
        time.sleep(10)

        # 6. Click on the row options button using role="button"
        row_options_button = driver.find_element(By.CSS_SELECTOR, 'button[role="button"]')
        row_options_button.click()
        time.sleep(2)
        # 7. Send two arrow keys down
        action = ActionChains(driver)
        action.send_keys(Keys.ARROW_DOWN).perform()
        time.sleep(2)
        # 8. Send SPACEBAR
        action.send_keys(Keys.SPACE).perform()
        time.sleep(2)
        # 9. Send keys: "DELETE"
        action.send_keys("DELETE").perform()
        time.sleep(2)
        # 10. Click on the "Delete All" span element
        delete_all_span = driver.find_element(By.XPATH, '//span[text()="Delete All"]')
        delete_all_span.click()

    finally:
        # Give some time to observe results before quitting
        time.sleep(5)
        driver.quit()

if __name__ == "__main__":
    delete_apk_sauce()
