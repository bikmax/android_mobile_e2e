import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def get_confirmation_code():
    # Set up Chrome options for headless mode
    chrome_options = Options()
    #chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    #chrome_options.add_argument("--no-sandbox")  # Disable sandbox for running without GUI
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems


    # Setup WebDriver with the correct Service object for chromedriver path and options
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Step 1: Open the URL
        driver.get("https://app.tuta.com/mail")

        # Step 2: Wait for the email input field to be present and send the email
        email_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//input[@type="email"]'))
        )
        email_input.send_keys("tutatatata@tutamail.com")

        # Step 3: Wait for the password input field to be present and send the password
        password_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//input[@type="password"]'))
        )
        password_input.send_keys("pass")

        # Step 4: Wait for the login button to be clickable and click it
        login_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@title="Log in"]'))
        )
        login_button.click()

        time.sleep(5)  # Adjust this time if necessary to ensure the page has loaded

        # Step 5: Wait for the div containing "Код подтверждения" to be clickable and click it
        confirmation_code_div = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//div[contains(text(),"Код подтверждения")]'))
        )
        confirmation_code_div.click()

        # Wait for the email body to load
        time.sleep(10)  # Adjust time if needed for email content to load

        # Step 6: Get the entire text content from the page
        page_text = driver.find_element(By.XPATH, '//body').text

        # Step 7: Use regex to find the confirmation code between "Ваш код подтверждения:" and "info@e2e_test_proj.online"
        match = re.search(r"Ваш код подтверждения:\s*(\d{4})\s*info@e2e_test_proj.online", page_text)

        # If match is found, return the code as integer
        if match:
            confirmation_code = int(match.group(1))  # Extract the code
            return confirmation_code
        else:
            print("Code not found")
            return None


    finally:
        # Close the browser after the process
        driver.quit()



