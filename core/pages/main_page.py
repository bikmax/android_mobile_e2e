import base64
import io
import logging
import os
import random
import re
import string
import time
import traceback
from datetime import datetime, timedelta
from pathlib import Path
from typing import Union

import allure
from appium.webdriver.common.appiumby import AppiumBy

import numpy as np
from PIL import Image
from PIL import ImageChops
from appium.webdriver.clipboard_content_type import ClipboardContentType
from appium.webdriver.extensions.android.nativekey import AndroidKey
from selenium.common import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from appium.webdriver.webdriver import WebDriver

from ResultCollector import ResultCollector
from reporting.TelegramReport import TelegramReport
from core.data.test_data import TestData
from core.pages.base_page import BasePage

from selenium.webdriver.support.wait import WebDriverWait

from core.pages.base_test import BaseTest


# from tests.base_test import BaseTest


class MainPage(BasePage):
    # Test data
    confirm_code = TestData.confirm_code
    logging.basicConfig(level=logging.DEBUG)

    # Locators

    SUGGEST_GIFT_TO_FRIEND_BUTTON = (
        By.XPATH, '//android.widget.Button[@content-desc="Предложить другу"]'
    )

    SUGGEST_BUTTON = (
        By.XPATH, '//android.widget.Button[@content-desc="Предложить"]'
    )

    ADD_TO_WISHES_BUTTON = (
        By.XPATH, '//android.widget.Button[@content-desc="Добавить в желания"]'
    )

    TRANSFER_TO_ANOTHER_WISH = (
        By.XPATH, '//android.widget.Button[@content-desc="Перевести на другое"]'
    )

    MAKE_TRANSFER = (
        By.XPATH, '//android.widget.Button[@content-desc="Сделать перевод"]'
    )

    DELETE_WISH = (
        By.XPATH, '//android.widget.Button[@content-desc="Удалить"]'
    )

    ADD_TO_WISHES_OR_BUY_BUTTON = (
        By.XPATH, '//android.widget.Button[@content-desc="В желания или купить"]'
    )

    ADD_TO_SELF_OR_BUY_BUTTON = (
        By.XPATH, '//android.widget.Button[@content-desc="Добавить к себе или купить"]'
    )

    RESERVE_WISH_BUTTON = (
        By.XPATH, '//android.widget.Button[@content-desc="Исполнить"]'
    )

    RESERVE_WISH_BUTTON_BONDS = "[335,1960][745,2120]"

    RESERVE_WISH_FINAL_BUTTON = (
        By.XPATH, '//android.widget.Button[@content-desc="Забронировать"]'
    )

    ACCEPT_RESERVED_WISH = (
        By.XPATH, '//android.widget.Button[@content-desc="Подтвердить"]'
    )

    OPEN_CUSTOM_WISH_LINK = (
        By.XPATH, '//android.view.View[@content-desc="Открыть ссылку"]'
    )

    DECLINE_RESERVED_WISH = (
        By.XPATH, '//android.widget.Button[@content-desc="Отменить"]'
    )

    ACCEPT_RESERVED_WISH_FINAL = "[307,2117][773,2277]"
    DECLINE_RESERVED_WISH_FINAL = (
        By.XPATH, '//android.widget.Button[@content-desc="Отменить"]'
    )

    PAY_FOR_WISH_BUTTON = (
        By.XPATH, '//android.widget.Button[@content-desc="Пополнить"]'
    )

    CONTRIBUTE_FOR_WISH_BUTTON = (
        By.XPATH, '//android.widget.Button[@content-desc="Поучаствовать"]'
    )

    PAY_GO_TO_PAYMENT_BUTTON = (
        By.XPATH, '//android.widget.Button[@content-desc="Перейти к оплате"]'
    )

    PAYMENT_EXECUTE_BUTTON = (
        By.XPATH, '//android.widget.Button[@content-desc="Исполнить"]'
    )

    ADD_WISH_WITHOUT_SETTINGS = (
        By.XPATH, '//android.view.View[contains(@content-desc, "настраивать")]'
    )
    CLOSE_WEBVIEW = (
        By.XPATH, '//android.widget.ImageButton[@content-desc="Close tab"]'
    )

    ADD_WISH_WITH_SETTINGS = (
        By.XPATH, '//android.view.View[contains(@content-desc, "приватность")]'
    )

    DESCRIPTION_FILED = (
        By.XPATH, '//android.widget.EditText'
    )

    PRIVACY_ALL = (
        By.XPATH, '//android.widget.ImageView[contains(@content-desc="Доступно всем")]'
    )

    PRIVACY_ONLY_ME = (
        By.XPATH, '//android.view.View[@content-desc="Доступно только мне Только у вас будет доступ"]'
    )
    PRIVACY_ONLY_ME_DESC = "Только у вас будет доступ"

    PRIVACY_SOME = (
        By.XPATH, '//android.widget.ImageView[contains(@content-desc="Доступно некоторым")]'
    )
    PRIVACY_SOME_DESC = "Выбранные друзья получат доступ"

    ADD_WISH_BUTTON = (
        By.XPATH, '//android.widget.Button[contains(@content-desc, "Добавить")]'
    )

    SUGGEST_WISH_BUTTON = (
        By.XPATH, '//android.view.View[@content-desc="Предложить\nсвоё новое желание"]'
    )

    ACCEPT_WISH_BUTTON = (
        By.XPATH, '//android.view.View[contains(@content-desc, "не настраивать")]'
    )

    ACCEPT_SUGG_WISH_BUTTON = (
        By.XPATH, '//android.widget.Button[@content-desc="Принять"]'
    )

    ACCEPT_1_WISH_BUTTON = (
        By.XPATH, '(//android.widget.Button[@content-desc="Принять"])[1]'
    )

    ACCEPT_2_WISH_BUTTON = (
        By.XPATH, '(//android.widget.Button[@content-desc="Принять"])[2]'
    )

    ADD_WISH_AGAIN_BUTTON = (
        By.XPATH, '//android.widget.Button[@content-desc="Добавить снова"]'
    )

    ADD_WISH_AGAIN_FINAL_BUTTON = (
        By.XPATH, '//android.widget.Button[@content-desc="Добавить"]'
    )

    FINAL_ACCEPT_BONDS = "[778,74][1080,200]"

    DECLINE_WISH_BUTTON = (
        By.XPATH, '//android.widget.Button[contains(@content-desc, "Отклонить")]'
    )

    ADD_CUSTOM_WISH_LINK = (
        By.XPATH, '//android.widget.EditText[@resource-id="custom_wish_link_field"]'
    )

    PHONE_NUMBER_BUTTON_LOCATOR = (
        By.XPATH,
        "//android.widget.FrameLayout[@resource-id='android:id/content']/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.widget.Button[1]"
    )
    CONTINUE_BUTTON_LOCATOR = (
        By.XPATH, '//android.widget.Button[@content-desc="Продолжить"]'
    )



    CONTINUE_SKIP_1 = (
        By.XPATH, '//android.view.View[contains(@content-desc, "каталога")]'
    )

    CONTINUE_SKIP_2 = (
        By.XPATH, '//android.view.View[contains(@content-desc, "ПОМОЩНИК")]'
    )

    CONTINUE_SKIP_3 = (
        By.XPATH, '//android.view.View[contains(@content-desc, "РАЗНЫЕ")]'
    )

    CONTINUE_SKIP_4 = (
        By.XPATH, '//android.view.View[contains(@content-desc, "ДОНАТЫ")]'
    )


    SKIP_BUTTON_LOCATOR = (
        By.XPATH, '//android.widget.Button[@content-desc="Пропустить"]'
    )

    CONFIRM_NUMBER_BUTTON_LOCATOR = (
        By.CLASS_NAME, "android.widget.EditText"
    )

    PROFILE_SETTINGS_LOCATOR = "main_page_profile_and_settings_button"

    PROFILE_FULL_USERNAME_LOCATOR = (
        By.XPATH, '//android.view.View[@content-desc="Firsty AAA"]'
    )

    MY_GROUPS_NO_GROUPS_TEXT = (
        By.XPATH, '//android.view.View[@content-desc="Создайте группу"]'
    )

    GIFT_LIST_LOCATOR = (
        By.XPATH, '//*[contains(@content-desc, "Список моих")]'
    )
    CHOOSE_FROM_CATALOG_BUTTON = (
        By.XPATH, '//*[contains(@content-desc, "Выбрать")]'
    )
    CATALOG_CATEGORIES_BUTTON = (
        By.XPATH, '//android.widget.ImageView[@content-desc="Категории"]'
    )
    CATALOG_3_BUTTON = (
        By.XPATH,
        '//android.widget.ScrollView/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[5]/android.widget.ImageView[3]'
    )
    CATALOG_1_BUTTON = (
        By.XPATH,
        '//android.widget.ScrollView/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[1]/android.widget.ImageView[1]'
    )
    CATALOG_2_BUTTON = (
        By.XPATH,
        '//android.widget.ScrollView/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[5]/android.widget.ImageView[2]'
    )
    CATALOG_4_BUTTON = (
        By.XPATH,
        '//android.widget.ScrollView/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[3]/android.widget.ImageView[1]'
    )
    ALL_FROM_CATEGORY = (
        By.XPATH, '//android.widget.ImageView[@content-desc="Всё из этой категории"]'
    )
    THIRD_GOOD = (
        By.XPATH,
        '//android.widget.ScrollView/android.view.View/android.view.View/android.view.View[2]/android.view.View/android.view.View[3]/android.view.View[2]'
    )
    FIRST_GOOD = (
        By.XPATH,
        '//android.widget.ScrollView/android.view.View/android.view.View/android.view.View[2]/android.view.View/android.view.View[3]/android.view.View[2]'
    )

    FIRST_PARTNER_GOOD = (
        By.XPATH, "//android.widget.ImageView[contains(@content-desc, 'Товар партнёра')]"
    )

    SECOND_GOOD = (
        By.XPATH,
        '//android.widget.ScrollView/android.view.View/android.view.View/android.view.View[2]/android.view.View/android.view.View[3]/android.view.View[2]'
    )
    FOURTH_GOOD = (
        By.XPATH,
        '//android.widget.ScrollView/android.view.View/android.view.View/android.view.View[2]/android.view.View/android.view.View[3]/android.view.View[2]'
    )

    HOME_BOTTOM_BUTTON = (
        By.XPATH, '//android.widget.ImageView[contains(@content-desc, "Вкладка 1")]'
    )
    HOME_BOTTOM_BUTTON_BOUNDS = "[0,2212][216,2353]"

    CATALOG_BOTTOM_BUTTON = (
        By.XPATH, '//android.widget.ImageView[@content-desc="Вкладка 2 из 5"]'
    )
    CATALOG_BOTTOM_BUTTON_BOUNDS = "[216,2212][432,2353]"

    AI_BOTTOM_BUTTON = (
        By.XPATH, '//android.widget.ImageView[contains(@content-desc, "Вкладка 3")]'
    )
    AI_BOTTOM_BUTTON_BOUNDS = "[432,1700][648,1857]"

    FRIENDS_BOTTOM_BUTTON = (
        By.XPATH, '//android.widget.ImageView[contains(@content-desc, "Вкладка 4")]'
    )
    FRIENDS_BOTTOM_BUTTON_BOUNDS = "[648,2208][864,2357]"

    WISH_BOTTOM_BUTTON = (
        By.XPATH, '//android.widget.ImageView[contains(@content-desc, "Вкладка 5")]'
    )
    WISH_BOTTOM_BUTTON_BOUNDS = "[864,2212][1080,2353]"

    FRIEND_CONTACT = (
        By.XPATH, '//android.view.View[contains(@content-desc, "Василий")]'
    )

    SUGGEST_WISH_TO_FRIEND = (
        By.XPATH, '//android.widget.Button[@content-desc="Предложить желание"]'
    )

    NOTIFICATION_WISH_SUGGESTED = (
        By.XPATH, '//android.widget.ImageView[contains(@content-desc, "Вам предложили желание")]'
    )

    NOTIFICATION_WISH_PAYMENT_COMPLETE = (
        By.XPATH, '//android.widget.ImageView[contains(@content-desc, "Ваше желание исполнено")]'
    )

    NOTIFICATION_FRIEND_WISH_PAYMENT_COMPLETE = (
        By.XPATH, '//android.widget.ImageView[contains(@content-desc, "Желание друга исполнено")]'
    )

    NOTIFICATION_NEW_DONATE_FROM_FRIEND = (
        By.XPATH, '//android.widget.ImageView[contains(@content-desc, "Новое накопление")]'
    )

    NOTIFICATION_PARTICIPATED_WISH_DELETED = (
        By.XPATH, '//android.widget.ImageView[contains(@content-desc, "Желание с участием удалено")]'
    )

    NOTIFICATION_YOU_RESERVED_FRIEND_WISH = (
        By.XPATH, '//android.widget.ImageView[@content-desc="Вы успешно забронировали желание друга"]'
    )

    NOTIFICATION_YOUR_RESERVED_WISH_DONE_AND_ARCHIVED = (
        By.XPATH, '//android.widget.ImageView[@content-desc="Ваше желание исполнено и перенесено в архив"]'
    )

    NOTIFICATION_RESERVED_WISH_AVAILABLE_AGAIN = (
        By.XPATH, '//android.widget.ImageView[@content-desc="Ваше желание снова доступно всем друзьям"]'
    )

    NOTIFICATION_WISH_SUGGESTED_TO_FRIEND = (
        By.XPATH, '//android.widget.ImageView[contains(@content-desc, "Товар успешно предложен вашему другу")]'
    )

    NOTIFICATION_WISH_FROM_FRIEND_ACCEPTED = (
        By.XPATH, '//android.widget.ImageView[contains(@content-desc, "принял ваше желание")]'
    )

    NOTIFICATION_SUPPORT_MESSAGE_SENT = (
        By.XPATH, '//android.widget.ImageView[@content-desc="Ваше сообщение было успешно отправлено в поддержку"]'
    )

    NOTIFICATION_GROUP_CREATED = (
        By.XPATH, '//android.widget.ImageView[@content-desc="Группа была создана"]'
    )

    NOTIFICATION_NEW_FRIEND_IN_APP = (
        By.XPATH, '//android.widget.ImageView[contains(@content-desc, "Новый друг в приложении")]'
    )

    NOTIFICATION_AVATAR_UPDATED = (
        By.XPATH, '//android.widget.ImageView[contains(@content-desc, "Ваш аватар успешно обновлен")]'
    )

    NOTIFICATION_PROFILE_DATA_UPDATED = (
        By.XPATH, '//android.widget.ImageView[contains(@content-desc, "Ваши данные успешно обновлены")]'
    )

    NOTIFICATION_WISH_ADDED = (
        By.XPATH, '//android.widget.ImageView[contains(@content-desc, "добавлен")]'
    )

    NOTIFICATION_WISH_DECLINED = (
        By.XPATH, '//android.widget.ImageView[contains(@content-desc, "Ваше предложение отклонено")]'
    )

    NOTIFICATION_FIREND_ADDED_WISH = (
        By.XPATH, '//android.widget.ImageView[contains(@content-desc, "Посмотрите новые желания")]'
    )

    NOTIFICATION_RESEND_CODE = (
        By.XPATH, '//android.widget.ImageView[contains(@content-desc, "Код успешно отправлен")]'
    )

    NOTIFICATION_5_YEARS = (
        By.XPATH, '//android.widget.ImageView[contains(@content-desc, "Пользователь должен быть старше 5 лет")]'
    )

    NOTIFICATION_WISH_DATA_UPDATED = (
        By.XPATH, '//android.widget.ImageView[contains(@content-desc, "Данные желания успешно изменены")]'
    )

    DONE_BUTTON = (
        By.XPATH, '//android.widget.Button[@content-desc="Готово"]'
    )

    NEXT_BUTTON = (
        By.XPATH, '//android.widget.Button[@content-desc="Далее"]'
    )

    SEE_BUTTON = (
        By.XPATH, '//android.widget.Button[@content-desc="Посмотреть"]'
    )

    SEE_BUTTON_1 = (
        By.XPATH, '(//android.widget.Button[@content-desc="Посмотреть"])[1]'
    )

    SEE_BUTTON_2 = (
        By.XPATH, '(//android.widget.Button[@content-desc="Посмотреть"])[2]'
    )

    SEE_BUTTON_3 = (
        By.XPATH, '(//android.widget.Button[@content-desc="Посмотреть"])[3]'
    )

    ADD_BUTTON = (
        By.XPATH, '//android.widget.Button[@content-desc="Добавить"]'
    )

    SEND_BUTTON = (
        By.XPATH, '//android.widget.Button[@content-desc="Отправить"]'
    )

    DELIVERY_FOUND_SELECTED_PICKUP_POINT_CHOOSE_BUTTON = (
        By.XPATH, '//android.widget.Button[@content-desc="Выбрать пункт"]'
    )

    SEE_SUGGESTED_WISH_FROM_NOTIFICATIONS = (
        By.XPATH, '//*[contains(@content-desc, "Посмотреть")]'
    )

    # Methods
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.driver = driver

    # Screenshot
    @staticmethod
    def generate_filename(base_name, action_taken, test_ss_name: str):
        return f"reporting/ss/{test_ss_name}/{base_name}_{action_taken}.png"

    def open_first_friend(self, driver):
        time.sleep(2)
        self.click(TestData.BOTTOM_FRIENDS_BTN_XP)
        time.sleep(2)
        self.swipe_down(1999)
        time.sleep(2)
        self.click(TestData.CONTACTS_FRIEND_1)
        time.sleep(2)

    def swipe_down(self, pixels: int):
        """
        Swipe down on the screen by a specified number of pixels.

        :param pixels: Number of pixels to swipe down.
        """
        window_size = self.driver.get_window_size()
        start_x = window_size['width'] / 2  # Swipe from the center horizontally
        start_y = window_size['height'] / 2  # Start in the middle of the screen
        end_y = start_y + pixels  # Swipe down by the specified pixels

        self.driver.swipe(start_x, start_y, start_x, end_y, 1000)

    def swipe_up(self, pixels: int):
        """
        Swipe up on the screen by a specified number of pixels.

        :param pixels: Number of pixels to swipe up.
        """
        window_size = self.driver.get_window_size()
        start_x = window_size['width'] / 2  # Swipe from the center horizontally
        start_y = window_size['height'] / 2  # Start in the middle of the screen
        end_y = start_y - pixels  # Swipe up by the specified pixels

        self.driver.swipe(start_x, start_y, start_x, end_y, 1000)

    def auth_by_phone(self, phone_number: str, confirm_code: str):
        """Authenticate by phone number and confirmation code."""
        self.is_element_visible(TestData.AUTH_BYPHONE)
        self.click(TestData.AUTH_BYPHONE)
        time.sleep(3)
        self.is_element_visible(TestData.AUTH_PHONE_FIELD)
        self.click(TestData.AUTH_PHONE_FIELD)
        time.sleep(1)

        # # Send 16 backspaces to clear the field
        # actions = ActionChains(self.driver)
        # for _ in range(16):
        #     actions.send_keys(Keys.BACKSPACE)
        #     actions.perform()
        #     time.sleep(0.1)  # Optional: Add a small delay between backspaces
        self.send_keys_simple(phone_number)

        time.sleep(5)

        self.is_element_visible(self.CONTINUE_BUTTON_LOCATOR)
        self.click(self.CONTINUE_BUTTON_LOCATOR)

        # Enter the confirmation code
        self.is_element_visible(TestData.CONFIRM_CODE)
        self.send_keys_simple(confirm_code)

    def auth_by_phone_with_skip_ob(self, phone_number: str, confirm_code: str):
        """Authenticate by phone number and confirmation code."""

        #self.is_element_visible(MainPage.CONTINUE_SKIP_1)
        self.is_element_visible(MainPage.CONTINUE_BUTTON_LOCATOR)
        self.click(MainPage.CONTINUE_BUTTON_LOCATOR)
        time.sleep(6)
        #self.is_element_visible(MainPage.CONTINUE_SKIP_2)
        self.is_element_visible(MainPage.CONTINUE_BUTTON_LOCATOR)
        self.click(MainPage.CONTINUE_BUTTON_LOCATOR)
        time.sleep(6)
        #self.is_element_visible(MainPage.CONTINUE_SKIP_3)
        self.is_element_visible(MainPage.CONTINUE_BUTTON_LOCATOR)
        self.click(MainPage.CONTINUE_BUTTON_LOCATOR)
        time.sleep(6)
        #self.is_element_visible(MainPage.CONTINUE_SKIP_4)
        self.is_element_visible(MainPage.CONTINUE_BUTTON_LOCATOR)
        self.click(MainPage.CONTINUE_BUTTON_LOCATOR)
        time.sleep(6)
        self.is_element_visible(TestData.AUTH_BYPHONE)
        self.click(TestData.AUTH_BYPHONE)
        time.sleep(5)
        self.is_element_visible(TestData.AUTH_PHONE_FIELD)
        self.click(TestData.AUTH_PHONE_FIELD)
        time.sleep(2)


        self.send_keys_simple(phone_number)

        time.sleep(2)

        self.is_element_visible(self.CONTINUE_BUTTON_LOCATOR)
        self.click(self.CONTINUE_BUTTON_LOCATOR)
        time.sleep(3)
        # Enter the confirmation code
        self.is_element_visible(TestData.CONFIRM_CODE)
        self.send_keys_simple(confirm_code)

    def skip_onboarding(self):
        """Skip onboarding screens by tapping 'Continue' until reaching the phone number input screen."""
        self.is_element_visible(MainPage.CONTINUE_SKIP_1)
        self.is_element_visible(MainPage.CONTINUE_BUTTON_LOCATOR)
        self.click(MainPage.CONTINUE_BUTTON_LOCATOR)

        self.is_element_visible(MainPage.CONTINUE_SKIP_2)
        self.is_element_visible(MainPage.CONTINUE_BUTTON_LOCATOR)
        self.click(MainPage.CONTINUE_BUTTON_LOCATOR)

        self.is_element_visible(MainPage.CONTINUE_SKIP_3)
        self.is_element_visible(MainPage.CONTINUE_BUTTON_LOCATOR)
        self.click(MainPage.CONTINUE_BUTTON_LOCATOR)

        self.is_element_visible(MainPage.CONTINUE_SKIP_4)
        self.is_element_visible(MainPage.CONTINUE_BUTTON_LOCATOR)
        self.click(MainPage.CONTINUE_BUTTON_LOCATOR)


    def open_first_friend_first_wish(self):
        time.sleep(1)
        self.is_element_visible(TestData.BOTTOM_FRIENDS_BTN_XP)
        self.click(TestData.BOTTOM_FRIENDS_BTN_XP)
        self.is_element_visible(TestData.CONTACTS_FRIEND_1)
        self.click(TestData.CONTACTS_FRIEND_1)
        self.is_element_visible(TestData.friend_wish_first_wish)
        self.click(TestData.friend_wish_first_wish)
        time.sleep(1)

    def open_second_friend_first_wish(self):
        time.sleep(1)
        self.is_element_visible(TestData.BOTTOM_FRIENDS_BTN_XP)
        self.click(TestData.BOTTOM_FRIENDS_BTN_XP)
        self.is_element_visible(TestData.CONTACTS_FRIEND_2)
        self.click(TestData.CONTACTS_FRIEND_2)
        self.is_element_visible(TestData.friend_wish_first_wish)
        self.click(TestData.friend_wish_first_wish)
        time.sleep(1)

    def click_by_uiautomator(self, resource_id: str, timeout: int = 30):
        """Кликает по элементу с указанным resource-id через UiSelector."""
        locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().resourceId("{resource_id}")')

        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
        except TimeoutException:
            screenshot_path = f"reporting/ss/click_by_uiautomator_{resource_id}.png"
            self.driver.save_screenshot(screenshot_path)
            print(f"Failed to click: {resource_id}. Screenshot saved: {screenshot_path}")
            raise

    def click_by_uiautomator_desc(self, description: str, timeout: int = 30):
        """Кликает по элементу с указанным description через UiSelector."""
        locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().description("{description}")')

        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
        except TimeoutException:
            screenshot_path = f"reporting/ss/click_by_uiautomator_desc_{description}.png"
            self.driver.save_screenshot(screenshot_path)
            print(f"Failed to click: {description}. Screenshot saved: {screenshot_path}")
            raise

    def click_by_uiautomator_desc_contains(self, partial_description: str, timeout: int = 30):
        """Кликает по элементу, у которого description содержит указанный текст через UiSelector."""
        locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().descriptionContains("{partial_description}")')

        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
        except TimeoutException:
            screenshot_path = f"reporting/ss/click_by_uiautomator_desc_contains_{partial_description}.png"
            self.driver.save_screenshot(screenshot_path)
            print(f"Failed to click: {partial_description}. Screenshot saved: {screenshot_path}")
            raise

    def click_by_accessibility_id(self, accessibility_id: str, timeout: int = 30):
        """Кликает по элементу с указанным accessibility id."""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, accessibility_id))
            )
            element.click()
        except TimeoutException:
            screenshot_path = f"reporting/ss/click_by_accessibility_id_{accessibility_id}.png"
            self.driver.save_screenshot(screenshot_path)
            print(f"Failed to click: {accessibility_id}. Screenshot saved: {screenshot_path}")
            raise

    def check_notification(self, driver, test_ss_name: str):
        """Проверить оповещение в колокольчике"""
        time.sleep(1)
        self.click(TestData.BOTTOM_HOME_BTN_XP)
        time.sleep(3)
        self.click(TestData.notification_bell)
        time.sleep(5)
        # Screenshot block
        action_taken = "_after_click_bell"
        ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
        ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
        self.take_element_screenshot_by_bounds(driver, TestData.main_screen_ss, ss_etalon)
        self.take_element_screenshot_by_bounds(driver, TestData.main_screen_ss, ss_run)
        time.sleep(1)
        assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

        self.click(MainPage.SEE_BUTTON)
        time.sleep(3)
        # Screenshot block
        action_taken = "_after_click_see"
        ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
        ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
        self.take_element_screenshot_by_bounds(driver, TestData.main_screen_ss, ss_etalon)
        self.take_element_screenshot_by_bounds(driver, TestData.main_screen_ss, ss_run)
        time.sleep(1)
        assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

    def generate_random_birthday(self):
        # Generate a random date
        start_date = datetime(1899, 1, 1)  # Earliest date
        end_date = datetime(2018, 12, 31)  # Latest date
        random_date = start_date + (end_date - start_date) * random.random()

        # Format the date as DDMMYYYY
        return random_date.strftime("%d%m%Y")

    def generate_birthday_soon(self, days_ahead: int):
        """Генерирует дату рождения с фиксированным годом 1990 и датой, которая наступит через указанное количество дней."""
        future_date = datetime.today() + timedelta(days=days_ahead)
        return future_date.strftime("%d%m") + "1990"

    def register_new_user(self, driver, phone_number):
        """Register new user from UI based on the given phone number."""

        # задаем имена для известных номеров
        name_mapping = {
            TestData.phone_friend1: "Firsty",
            TestData.phone_friend2: "Vtoroy",
            TestData.phone_friend3: "Tretiy"
        }

        if phone_number not in name_mapping:
            raise ValueError(f"Unexpected phone number: {phone_number}")

        user_name = name_mapping[phone_number]
        random_birthday = self.generate_random_birthday()

        time.sleep(2)
        self.is_element_visible(self.CONTINUE_BUTTON_LOCATOR)
        time.sleep(2)
        self.click(self.CONTINUE_BUTTON_LOCATOR)
        # TelegramReport.send_tg(f"click({self.CONTINUE_BUTTON_LOCATOR})")

        time.sleep(2)
        self.click(TestData.AUTH_CBX_TERMS)
        # TelegramReport.send_tg(f"click(TestData.AUTH_CBX_TERMS)")

        time.sleep(1)
        self.click(self.CONTINUE_BUTTON_LOCATOR)
        # TelegramReport.send_tg(f"click({self.CONTINUE_BUTTON_LOCATOR})")

        time.sleep(2)
        self.click(TestData.register_name)
        # TelegramReport.send_tg(f"click(TestData.register_name)")

        time.sleep(1)
        self.send_keys_simple(user_name)
        # TelegramReport.send_tg(f"Entered name: {user_name}")

        time.sleep(1)
        self.click_by_uiautomator(TestData.register_bday)
        time.sleep(1)
        # TelegramReport.send_tg(f"click_by_uiautomator(TestData.register_bday)")

        self.send_keys_simple(random_birthday)
        # TelegramReport.send_tg(f"Entered birthday: {random_birthday}")

        # Закрытие клавиатуры
        self.driver.hide_keyboard()
        time.sleep(1)

        # Продолжение выполнения свайпа
        self.scroll_until_visible(driver, self.CONTINUE_BUTTON_LOCATOR)
        self.click(self.CONTINUE_BUTTON_LOCATOR)

    def register_new_user_all_fields(self, driver, name: str, second_name: str, email: str):
        """Register new user from UI"""
        screenshot_path = "reporting/ss/"

        time.sleep(2)
        self.click(self.CONTINUE_BUTTON_LOCATOR)
        # TelegramReport.send_tg(f"click({self.CONTINUE_BUTTON_LOCATOR})")
        time.sleep(2)
        self.click(TestData.AUTH_CBX_TERMS)
        # TelegramReport.send_tg(f"click(TestData.AUTH_CBX_TERMS)")
        time.sleep(2)
        self.click(self.CONTINUE_BUTTON_LOCATOR)
        # TelegramReport.send_tg(f"click({self.CONTINUE_BUTTON_LOCATOR})")
        time.sleep(2)
        # name
        self.click(TestData.register_name)
        # TelegramReport.send_tg(f"clickTestData.register_name)")
        time.sleep(2)
        self.send_keys_simple(name)
        time.sleep(1)
        # second name
        self.click(TestData.register_second_name)
        # TelegramReport.send_tg(f"clickTestData.register_second_name)")
        time.sleep(2)
        self.send_keys_simple(second_name)
        time.sleep(1)
        # bday
        time.sleep(2)
        self.click_by_uiautomator(TestData.register_bday)
        time.sleep(2)
        # TelegramReport.send_tg(f"clickTestData.register_bday)")
        self.send_keys_simple("11111999")
        time.sleep(2)
        self.driver.hide_keyboard()
        time.sleep(2)
        # email
        # self.swipe_up(400)
        # self.click_by_uiautomator(TestData.register_email_id)
        # TelegramReport.send_tg(f"clickTestData.register_email)")
        # time.sleep(2)
        # self.send_keys_simple(email)
        # time.sleep(1)
        # self.driver.hide_keyboard()
        time.sleep(1)

        self.scroll_until_visible(driver, self.CONTINUE_BUTTON_LOCATOR)
        self.click(self.CONTINUE_BUTTON_LOCATOR)

        # Step 5: Take a screenshot after entering the confirmation code
        #self.take_screenshot(f"{screenshot_path}confirm_code_1_enter.png")

    def logout(self, driver):
        """Logout."""
        time.sleep(1)
        self.is_element_visible(TestData.BOTTOM_HOME_BTN)
        self.click_by_uiautomator(TestData.BOTTOM_HOME_BTN)

        self.is_element_visible(self.PROFILE_SETTINGS_LOCATOR)
        self.click_by_uiautomator(self.PROFILE_SETTINGS_LOCATOR)

        self.is_element_visible(TestData.logout_button)
        self.click(TestData.logout_button)

        self.is_element_visible(TestData.logout_confirm_button)
        self.click(TestData.logout_confirm_button)
        time.sleep(1)

    def click(self, locator: tuple | str):
        try:
            if isinstance(locator, str):  # Если передан resource-id, формируем UiSelector
                locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().resourceId("{locator}")')

            # Ожидание кликабельности
            element = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable(locator))
            time.sleep(1)
            element.click()
            time.sleep(1)
        except TimeoutException:
            print(f"Element {locator} not clickable. Trying to scroll to it...")

            if self.scroll_until_visible(self.driver, locator):  # Прокрутка к элементу
                try:
                    element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(locator))
                    time.sleep(1)
                    element.click()
                except TimeoutException:
                    pass  # Если всё ещё не кликабельно, обработка ошибки ниже
            raise

    def click_on_friend(self, phone_number: str):
        """Click on an element containing a phone number with timeout and take a screenshot after the click."""
        screenshot_path = "reporting/ss/"

        # Generate XPath for the phone number dynamically within content-desc
        locator = (By.XPATH, f"//android.view.View[contains(@content-desc, '{phone_number}')]")

        # Sanitize phone number for filename
        locator_name = phone_number.replace("/", "_").replace(" ", "_")  # Sanitize phone number for filename
        action_name = "click"
        filename = f"{screenshot_path}{action_name}_phone_{locator_name}.png"

        try:
            # Wait for the element containing the phone number to be clickable
            element = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located(locator))
            element = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable(locator))
            element.click()
        except TimeoutException:
            # Take a screenshot on failure
            print(f"Element with phone number {phone_number} not clickable within 30 seconds.")
            self.driver.save_screenshot(filename)
            raise

        # Take a screenshot after the click attempt
        self.driver.save_screenshot(filename)

    def click_element_by_phone_number_contains(self, partial_phone_number: str):
        """
        Click an element on the page by dynamically generating its locator using a partial phone number.
        """
        screenshot_path = "reporting/ss/"
        locator_value = f'//android.widget.CheckBox[contains(@content-desc, "{partial_phone_number}")]'
        locator = (By.XPATH, locator_value)

        # Sanitize locator for screenshot filename
        locator_name = partial_phone_number.replace("/", "_").replace(" ", "_")
        action_name = "click"
        filename = f"{screenshot_path}{action_name}_xpath_{locator_name}.png"

        try:
            # Wait for the element to be clickable and click it
            element = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
        except TimeoutException:
            # Take a screenshot on failure
            print(f"Element containing phone number {partial_phone_number} not clickable within 30 seconds.")
            self.driver.save_screenshot(filename)
            raise
        else:
            # Take a screenshot after successful click
            self.driver.save_screenshot(filename)

    def send_keys(self, locator: tuple, value: str):
        """Send keys to an input element."""
        element = self.wait.until(EC.presence_of_element_located(locator))
        element.clear()
        element.send_keys(value)

    @staticmethod
    def clear_text_field_simple(driver):
        """
        Sends Ctrl+A and Delete regardless of the target element to clear the text in focus.

        :param driver: Selenium WebDriver instance
        """
        try:
            actions = ActionChains(driver)
            actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL)  # Use Keys.COMMAND for macOS
            actions.send_keys(Keys.DELETE).perform()
            status = "🟢"
        except Exception as e:
            raise RuntimeError(f"Failed to clear the text field: {str(e)}")

    def send_keys_simple(self, value: str):
        """
        Send keys to the page regardless of the target element, with a 1-second delay between each key press.

        :param value: The string value to send.
        """
        time.sleep(1)
        actions = ActionChains(self.driver)

        for char in value:
            actions.send_keys(char)
            actions.perform()
            time.sleep(0.15)  # Add a 1-second delay between key presses

    def copy_paste_simple(self, value: str):
        """
        Copy text to the clipboard and paste it into the currently focused field.

        :param value: The string value to send.
        """
        # Set the clipboard text
        self.driver.set_clipboard_text(value, ClipboardContentType.PLAINTEXT)

        # Use ActionChains to paste the text
        actions = ActionChains(self.driver)
        actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

    def scroll_down(self, driver, num_screens=1):
        """
        Scroll a fixed number of screens down, including fractional screen scrolls.

        :param driver: The Appium driver instance.
        :param num_screens: Number of screens to scroll down (e.g., 1, 2, 0.5, etc.).
        """
        # Get the window size
        window_size = driver.get_window_size()
        start_y = window_size['height'] * 0.8
        end_y = window_size['height'] * 0.2

        # Calculate the amount to scroll based on the number of screens
        scroll_distance = (start_y - end_y) * num_screens

        print(f"Window Size: {window_size}")
        print(f"Start Y: {start_y}, End Y: {end_y}, Scroll Distance: {scroll_distance}")

        # Perform the swipe action using driver.swipe
        driver.swipe(
            start_x=window_size['width'] / 2,  # Start swipe at the center of the screen
            start_y=start_y,  # Start at the top part of the screen
            end_x=window_size['width'] / 2,  # End at the center of the screen (no horizontal movement)
            end_y=start_y - scroll_distance,  # Scroll down
            duration=800  # Duration of the swipe in milliseconds
        )

    def scroll_until_visible(self, driver, element_locator, max_scrolls=10, swipe_duration=1000, swipe_pause=2):
        """
        Scroll the screen until the element is visible or the maximum number of scrolls is reached.

        :param driver: The Appium driver instance.
        :param element_locator: The locator of the element to be found.
        :param max_scrolls: Maximum number of scroll attempts to avoid infinite loops.
        :param swipe_duration: Duration of swipe in milliseconds (higher = slower swipe).
        :param swipe_pause: Pause time between swipes in seconds.
        :return: True if the element becomes visible, False otherwise.
        """
        for _ in range(max_scrolls):
            try:
                # Check if the element is visible
                if driver.find_element(*element_locator).is_displayed():
                    return True
            except Exception:
                pass

            # Perform the scroll action
            window_size = driver.get_window_rect()
            start_x = window_size['width'] / 2
            start_y = window_size['height'] * 0.8
            end_y = window_size['height'] * 0.2

            driver.swipe(start_x, start_y, start_x, end_y, swipe_duration)
            time.sleep(swipe_pause)
        return False

    def take_screenshot(self, filename: str):
        """Take a screenshot and save it to the specified file."""
        self.driver.save_screenshot(filename)

    def is_element_visible(self, locator: tuple | str, timeout: int = 30) -> bool:
        """
        Проверяет видимость элемента на экране с кастомным таймаутом
        """
        if isinstance(locator, str):
            locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().resourceId("{locator}")')

        time.sleep(1)
        WebDriverWait(
            self.driver,
            timeout=timeout,
            poll_frequency=0.3,
            ignored_exceptions=[
                NoSuchElementException,
                StaleElementReferenceException
            ]
        ).until(EC.visibility_of_element_located(locator))
        time.sleep(1)
        return True

    def is_element_visible_by_description(self, description: str, timeout: int = 30) -> bool:
        """
        Проверяет, виден ли элемент по description (accessibility id).
        Использует UiSelector().description("...").
        """
        locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().description("{description}")')

        try:
            WebDriverWait(
                self.driver,
                timeout=timeout,
                poll_frequency=0.3,
                ignored_exceptions=[
                    NoSuchElementException,
                    StaleElementReferenceException
                ]
            ).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            screenshot_path = f"reporting/ss/is_visible_by_desc_{description}.png"
            self.driver.save_screenshot(screenshot_path)
            print(f"[❌] Element with description '{description}' not visible. Screenshot saved: {screenshot_path}")
            return False

    def is_element_visible_by_resource_id(self, resource_id: str, timeout: int = 30) -> bool:
        """
        Проверяет, виден ли элемент по resource-id.
        Использует UiSelector().resourceId("...").
        """
        locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().resourceId("{resource_id}")')

        try:
            WebDriverWait(
                self.driver,
                timeout=timeout,
                poll_frequency=0.3,
                ignored_exceptions=[
                    NoSuchElementException,
                    StaleElementReferenceException
                ]
            ).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            screenshot_path = f"reporting/ss/is_visible_by_resource_{resource_id}.png"
            self.driver.save_screenshot(screenshot_path)
            print(f"[❌] Element with resource-id '{resource_id}' not visible. Screenshot saved: {screenshot_path}")
            return False

    def is_element_invisible(self, locator: Union[str, tuple]) -> bool:
        """
        Проверяет, что элемент невидим или отсутствует на странице, ожидая до 60 секунд.

        :param locator: resource-id (str) или кортеж (By, value)
        :return: True, если элемент невидим, иначе False.
        """
        time.sleep(1)
        if isinstance(locator, str):
            # Если передали строку, считаем, что это resource-id для UiAutomator
            locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().resourceId("{locator}")')

        try:
            print(f"Checking invisibility of locator: {locator}")  # Отладочный вывод
            WebDriverWait(self.driver, 90).until(EC.invisibility_of_element_located(locator))
            time.sleep(1)
            return True
        except TimeoutException:
            print(f"Element with locator {locator} is still visible or present after 60 seconds.")
            return False

    def click_element_by_bounds(self, bounds: str):
        """
        Click an element using its bounds with W3C Actions.

        :param bounds: The bounds of the element as a string, e.g., "[648,1708][864,1849]".
        """
        # Parse bounds
        bounds = bounds.strip("[]").split("][")
        top_left = list(map(int, bounds[0].split(",")))
        bottom_right = list(map(int, bounds[1].split(",")))

        # Calculate center coordinates
        center_x = (top_left[0] + bottom_right[0]) // 2
        center_y = (top_left[1] + bottom_right[1]) // 2

        # Create a touch pointer action using W3C actions
        pointer = PointerInput(interaction.POINTER_TOUCH, "touch")

        # Build the actions
        action_builder = ActionChains(self.driver)
        action_builder.w3c_actions = action_builder.w3c_actions or ActionBuilder(self.driver, mouse=pointer)

        # Add the move and click actions
        action_builder.w3c_actions.pointer_action.move_to_location(center_x, center_y)
        action_builder.w3c_actions.pointer_action.pointer_down()
        action_builder.w3c_actions.pointer_action.release()

        # Perform the action
        action_builder.perform()

    @staticmethod
    def take_element_screenshot_by_bounds(driver, bounds, save_path):
        """
        Делает скриншот элемента на основе координат и сохраняет его.

        :param driver: Инстанс Appium WebDriver.
        :param bounds: Координаты элемента в формате строки "[x1,y1][x2,y2]".
        :param save_path: Путь для сохранения скриншота.
        """
        # Убедиться, что директория существует
        directory = os.path.dirname(save_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Преобразовать bounds из строки в список координат
        match = re.findall(r"\[(\d+),(\d+)]", bounds)  # Убираем экранирование для ']'
        if not match or len(match) != 2:
            raise ValueError("Bounds должны быть в формате '[x1,y1][x2,y2]'")

        x1, y1 = map(int, match[0])
        x2, y2 = map(int, match[1])

        # Сделать общий скриншот экрана
        screenshot = driver.get_screenshot_as_png()
        screenshot = Image.open(io.BytesIO(screenshot))

        # Обрезать изображение по координатам
        element_screenshot = screenshot.crop((x1, y1, x2, y2))

        # Сохранить результат
        element_screenshot.save(save_path)

    @staticmethod
    def compare_screenshots(screenshot_path, reference_image_path, tolerance=10):
        """
        Сравнивает два изображения на основе пикселей и выводит разницу.
        :param screenshot_path: Путь к скриншоту, который нужно сравнить.
        :param reference_image_path: Путь к эталонному изображению.
        :param tolerance: Допуск на различия между изображениями (в процентах).
        :return: True, если изображения одинаковые в пределах допуска, иначе False.
        """
        # Открываем изображения
        screenshot = Image.open(screenshot_path).convert("RGB")
        reference_image = Image.open(reference_image_path).convert("RGB")

        # Приводим изображения к одинаковому размеру, если это необходимо
        if screenshot.size != reference_image.size:
            reference_image = reference_image.resize(screenshot.size)

        # Используем ImageChops для вычисления различий
        diff = ImageChops.difference(screenshot, reference_image)

        # Преобразуем разницу в массив numpy
        diff_array = np.array(diff)

        # Вычисляем среднее количество различий
        diff_count = np.sum(diff_array > 0)

        # Вычисляем процент различий
        total_pixels = diff_array.size
        diff_percentage = (diff_count / total_pixels) * 100

        print(f"Различие в процентах: {diff_percentage:.2f}%")

        # Если различие больше допуска, считаем, что изображения не совпадают
        if diff_percentage > tolerance:
            print("Скриншоты не совпадают.")
            return False
        else:
            print("Скриншоты совпадают в пределах допуска.")
            return True

    def clear_text_field(self):
        """
        Clears the text in the currently focused text field using select all and delete.

        Args:
            driver: The Appium WebDriver instance.
        """
        # Send 16 backspaces to clear the field
        actions = ActionChains(self.driver)
        for _ in range(25):
            actions.send_keys(Keys.BACKSPACE)
            actions.perform()
            time.sleep(0.1)

    def send_enter_key(self, driver):
        """
        Sends the ENTER key to the currently focused text field or element.

        Args:
            driver: The Appium WebDriver instance.
        """
        # Get the currently focused element
        active_element = driver.switch_to.active_element

        # Send the ENTER key
        active_element.send_keys(Keys.ENTER)

    def pay_by_card(self):
        with allure.step("Переключение на WebView для ввода данных карты"):
            #TelegramReport.send_tg("🔁 Начинаем оплату: возврат в NATIVE_APP")
            try:
                self.driver.switch_to.context("NATIVE_APP")
            except Exception as e:
                TelegramReport.send_tg(f"⚠️ Не удалось вернуться в NATIVE_APP: {str(e)}")

            time.sleep(5)  # Подождать пока WebView перерисуется

            contexts = self.driver.contexts
            #TelegramReport.send_tg(f"📡 Contexts: {contexts}")

            webview_context = None
            for context in contexts:
                if "WEBVIEW_ru.e2e_test_proj.dev" in context:
                    webview_context = context
                    break

            if not webview_context:
                raise Exception("❌ WebView контекст не найден")

            #TelegramReport.send_tg(f"🔍 Доступные контексты: {contexts}")
            self.driver.switch_to.context(webview_context)
            #TelegramReport.send_tg(f"✅ Переключились в контекст: {webview_context}")

            try:
                window_handles = self.driver.window_handles
                #TelegramReport.send_tg(f"🪟 WebView window handles: {window_handles}")

                if not window_handles:
                    raise Exception("❌ Нет доступных окон в WebView")

                self.driver.switch_to.window(window_handles[0])
                #TelegramReport.send_tg(f"🔁 Переключились на окно {window_handles[0]}")

                # Проверим, что WebView живой и URL доступен
                current_url = self.driver.execute_script("return window.location.href")
                #TelegramReport.send_tg(f"🌐 WebView URL: {current_url}")

            except Exception as e:
                TelegramReport.send_tg(f"❌ WebView не отвечает: {str(e)}")
                raise

            # Галка "Сохранить карту"
            try:
                self.is_element_visible(TestData.save_card_button)
                self.click(TestData.save_card_button)
                #TelegramReport.send_tg("✅ Нажата галка 'Сохранить карту'")
            except Exception as e:
                TelegramReport.send_tg(f"❌ Не удалось нажать 'Сохранить карту': {str(e)}")
                raise

            # Ввод данных карты
            try:
                card_number_label = WebDriverWait(self.driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@class='t-label']"))
                )
                card_number_label.click()
                time.sleep(1)

                self.send_keys_simple(TestData.cardNumber)
                time.sleep(0.5)
                self.send_keys_simple(TestData.cardExpDate)
                time.sleep(0.5)
                self.send_keys_simple(TestData.cardCVC)
                time.sleep(0.5)

                self.driver.hide_keyboard()
                # #TelegramReport.send_tg("📥 Данные карты введены")
            except Exception as e:
                TelegramReport.send_tg(f"❌ Ошибка ввода карты: {str(e)}")
                raise

            # Клик "Оплатить"
            try:
                pay_button = WebDriverWait(self.driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@automation-id='card-form__submit']"))
                )
                pay_button.click()
                #TelegramReport.send_tg("💳 Нажата кнопка 'Оплатить'")
            except Exception as e:
                TelegramReport.send_tg(f"❌ Кнопка 'Оплатить' не нажата: {str(e)}")
                raise

            # Вернуться в NATIVE_APP
            try:
                self.driver.switch_to.context("NATIVE_APP")
                # #TelegramReport.send_tg("🔙 Вернулись в NATIVE_APP")
            except Exception as e:
                TelegramReport.send_tg(f"⚠️ Не удалось вернуться в NATIVE_APP: {str(e)}")

            # Подтверждение успеха
            try:
                success_message = WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, '//android.view.View[@content-desc="Всё успешно"]'))
                )
                time.sleep(1)
                horosho_button = WebDriverWait(self.driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, '//android.widget.Button[@content-desc="Хорошо"]'))
                )
                horosho_button.click()
                #TelegramReport.send_tg("✅ Оплата успешно завершена")
            except Exception as e:
                TelegramReport.send_tg(f"⚠️ Не удалось подтвердить успешную оплату: {str(e)}")
                raise

    def proceed_feedback(self):
        with allure.step("Прохождение опросника во WebView"):
            TelegramReport.send_tg("🚀 Начинаем прохождение опроса")

            time.sleep(5)  # Ждём, пока WebView появится

            contexts = self.driver.contexts
            TelegramReport.send_tg(f"📡 Контексты: {contexts}")

            webview_context = None
            for context in contexts:
                if "WEBVIEW_ru.e2e_test_proj.dev" in context:
                    webview_context = context
                    break

            if not webview_context:
                raise Exception("❌ WebView контекст не найден")

            self.driver.switch_to.context(webview_context)
            TelegramReport.send_tg(f"✅ Переключились в WebView: {webview_context}")

            self.driver.switch_to.window(self.driver.window_handles[0])

            # Универсальные хелперы
            def click_by_text(text, timeout=30):
                elem = WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable((By.XPATH, f"//*[text()='{text}']"))
                )
                elem.click()
                time.sleep(0.5)

            def type_in_textarea(message):
                textarea = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//textarea"))
                )
                textarea.click()
                textarea.clear()
                textarea.send_keys(message)
                time.sleep(0.5)

            def scroll_down():
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(0.7)

            # Пошаговая реализация
            click_by_text("Предложить улучшение")
            scroll_down()
            type_in_textarea("улучшение ГБ")
            click_by_text("Далее")
            click_by_text("сильно расстроюсь")
            click_by_text("Далее")
            click_by_text("5")
            click_by_text("Далее")
            click_by_text("да")
            click_by_text("5")
            type_in_textarea("улучшение добавления желания ГБ")
            scroll_down()
            click_by_text("Далее")
            click_by_text("да")
            click_by_text("5")
            type_in_textarea("улучшение вишлиста  ГБ")
            scroll_down()
            click_by_text("Далее")
            click_by_text("да")
            click_by_text("5")
            type_in_textarea("улучшение ИИ  ГБ")
            scroll_down()
            click_by_text("Далее")
            click_by_text("да")
            click_by_text("5")
            type_in_textarea("улучшение сбор средств  ГБ")
            scroll_down()
            click_by_text("Далее")
            click_by_text("Увидел рекламу")
            click_by_text("Далее")
            click_by_text("Да")
            type_in_textarea("офигенно")
            click_by_text("Я бы, наверное, не стал использовать альтернативу")
            click_by_text("Далее")
            type_in_textarea("эмоции")
            click_by_text("Далее")
            type_in_textarea("обычные люди")
            click_by_text("Далее")
            type_in_textarea("@maksotb")
            click_by_text("Далее")
            click_by_text("Вернуться в e2e_test_proj")

            TelegramReport.send_tg("✅ Опрос успешно пройден")

            self.driver.switch_to.context("NATIVE_APP")
            self.is_element_visible(TestData.BOTTOM_WISHES_BTN)

    def add_two_wishes(self):
        # Добавление желания
        with allure.step("Нажатие кнопки нижнего меню каталога"):
            time.sleep(1)
            self.is_element_visible(TestData.BOTTOM_CATALOG_BTN)
            self.click(TestData.BOTTOM_CATALOG_BTN)
            # TelegramReport.send_tg("click(MainPage.CATALOG_BOTTOM_BUTTON_BOUNDS)")

        with allure.step("Выбор категории товаров"):
            self.is_element_visible(TestData.CATALOG_CATEGORIES_BTN)
            self.click(TestData.CATALOG_CATEGORIES_BTN)
            # TelegramReport.send_tg("CATALOG_CATEGORIES_BUTTON clicked on phone 1")

        with allure.step("Выбор категории товара"):
            self.is_element_visible(TestData.CATEGORY_LIST_ITEM_1)
            self.click_by_uiautomator(TestData.CATEGORY_LIST_ITEM_1)
            # TelegramReport.send_tg("CATALOG_LIGHT_BUTTON clicked on phone 1")

        with allure.step("Выбор товара"):
            time.sleep(1)
            self.is_element_visible_by_resource_id(TestData.CATEGORY_ITEM_1)
            self.click_by_uiautomator(TestData.CATEGORY_ITEM_1)
            time.sleep(5)
            # TelegramReport.send_tg("goods_list_first_good clicked on phone 1")

        with allure.step("Прокрутка до кнопки добавления в желания"):
            self.scroll_until_visible(self.driver, MainPage.ADD_TO_WISHES_BUTTON)
            self.is_element_visible(MainPage.ADD_TO_WISHES_BUTTON)
            self.click(MainPage.ADD_TO_WISHES_BUTTON)
            # TelegramReport.send_tg("ADD_TO_WISHES_BUTTON clicked on phone 1")

        with allure.step("Добавление желания без настроек"):
            self.is_element_visible(MainPage.ADD_WISH_WITHOUT_SETTINGS)
            self.click(MainPage.ADD_WISH_WITHOUT_SETTINGS)
            # TelegramReport.send_tg("ADD_WISH_WITHOUT_SETTINGS clicked on phone 1")
            # self.is_element_visible(MainPage.NOTIFICATION_WISH_ADDED)
            # self.is_element_invisible(MainPage.NOTIFICATION_WISH_ADDED)

        with allure.step("Прокрутка до кнопки добавления в желания"):
            self.scroll_until_visible(self.driver, MainPage.ADD_TO_WISHES_BUTTON)
            self.is_element_visible(MainPage.ADD_TO_WISHES_BUTTON)
            self.click(MainPage.ADD_TO_WISHES_BUTTON)
            # TelegramReport.send_tg("ADD_TO_WISHES_BUTTON clicked on phone 1")

        with allure.step("Добавление желания без настроек"):
            self.is_element_visible(MainPage.ADD_WISH_WITHOUT_SETTINGS)
            self.click(MainPage.ADD_WISH_WITHOUT_SETTINGS)
            #self.is_element_visible(MainPage.NOTIFICATION_WISH_ADDED)
            time.sleep(1)

    def suggest_wish_to_friend_1(self):
        # Добавление желания
        with allure.step("Нажатие кнопки нижнего меню каталога"):
            time.sleep(1)
            self.click(TestData.BOTTOM_FRIENDS_BTN_XP)
            # TelegramReport.send_tg("click(MainPage.CATALOG_BOTTOM_BUTTON_BOUNDS)")

        with allure.step("Выбор CONTACTS_FRIEND_1"):
            self.is_element_visible(TestData.CONTACTS_FRIEND_1)
            self.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
            # TelegramReport.send_tg("CATALOG_CATEGORIES_BUTTON clicked on phone 1")

        with allure.step("Выбор SUGGEST_WISH_TO_FRIEND"):
            self.is_element_visible(MainPage.SUGGEST_WISH_TO_FRIEND)
            self.click(MainPage.SUGGEST_WISH_TO_FRIEND)
            # TelegramReport.send_tg("CATALOG_LIGHT_BUTTON clicked on phone 1")

        with allure.step("Выбор CHOOSE_FROM_CATALOG_BUTTON"):
            self.is_element_visible(MainPage.CHOOSE_FROM_CATALOG_BUTTON)
            self.click(MainPage.CHOOSE_FROM_CATALOG_BUTTON)
            # TelegramReport.send_tg("goods_list_first_good clicked on phone 1")

        with allure.step("Выбор категории товаров"):
            self.is_element_visible(TestData.CATALOG_CATEGORIES_BTN)
            self.click(TestData.CATALOG_CATEGORIES_BTN)
            # TelegramReport.send_tg("CATALOG_CATEGORIES_BUTTON clicked on phone 1")

        with allure.step("Выбор категории товара"):
            self.is_element_visible(TestData.CATEGORY_LIST_ITEM_1)
            self.click_by_uiautomator(TestData.CATEGORY_LIST_ITEM_1)
            # TelegramReport.send_tg("CATALOG_LIGHT_BUTTON clicked on phone 1")

        with allure.step("Выбор товара"):
            self.is_element_visible(TestData.CATEGORY_ITEM_2)
            self.click(TestData.CATEGORY_ITEM_2)
            time.sleep(5)
            # TelegramReport.send_tg("goods_list_first_good clicked on phone 1")

        with allure.step("Прокрутка до кнопки SUGGEST_GIFT_TO_FRIEND_BUTTON"):
            self.scroll_until_visible(self.driver, MainPage.SUGGEST_GIFT_TO_FRIEND_BUTTON)
            self.is_element_visible(MainPage.SUGGEST_GIFT_TO_FRIEND_BUTTON)
            self.click(MainPage.SUGGEST_GIFT_TO_FRIEND_BUTTON)
            # TelegramReport.send_tg("ADD_TO_WISHES_BUTTON clicked on phone 1")

        with allure.step("Добавление желания без настроек"):
            self.is_element_visible(MainPage.SUGGEST_BUTTON)
            self.click(MainPage.SUGGEST_BUTTON)
            # self.is_element_visible(MainPage.NOTIFICATION_WISH_SUGGESTED_TO_FRIEND)
            # self.is_element_invisible(MainPage.NOTIFICATION_WISH_SUGGESTED_TO_FRIEND)
            time.sleep(1)

    def accept_first_wish_privacy_onlyme(self):
        # Добавление желания
        with allure.step("Нажатие кнопки нижнего меню каталога"):
            time.sleep(1)
            self.click(TestData.BOTTOM_WISHES_BTN)
            # TelegramReport.send_tg("click(MainPage.CATALOG_BOTTOM_BUTTON_BOUNDS)")

        with allure.step("Выбор ACCEPT_WISH_BUTTON"):
            self.is_element_visible(MainPage.ACCEPT_WISH_BUTTON)
            self.click(MainPage.ACCEPT_WISH_BUTTON)
            # TelegramReport.send_tg("CATALOG_CATEGORIES_BUTTON clicked on phone 1")

        with allure.step("Выбор SUGGEST_WISH_TO_FRIEND"):
            self.is_element_visible(MainPage.ADD_WISH_WITH_SETTINGS)
            self.click(MainPage.ADD_WISH_WITH_SETTINGS)
            # TelegramReport.send_tg("CATALOG_LIGHT_BUTTON clicked on phone 1")

        with allure.step("Выбор CHOOSE_FROM_CATALOG_BUTTON"):
            self.is_element_visible(MainPage.CHOOSE_FROM_CATALOG_BUTTON)
            self.click(MainPage.CHOOSE_FROM_CATALOG_BUTTON)
            # TelegramReport.send_tg("goods_list_first_good clicked on phone 1")

        with allure.step("Выбор категории товаров"):
            self.is_element_visible(TestData.CATALOG_CATEGORIES_BTN)
            self.click(TestData.CATALOG_CATEGORIES_BTN)
            # TelegramReport.send_tg("CATALOG_CATEGORIES_BUTTON clicked on phone 1")

        with allure.step("Выбор категории товара"):
            self.is_element_visible(TestData.CATEGORY_LIST_ITEM_1)
            self.click_by_uiautomator(TestData.CATEGORY_LIST_ITEM_1)
            # TelegramReport.send_tg("CATALOG_LIGHT_BUTTON clicked on phone 1")

        with allure.step("Выбор товара"):
            self.is_element_visible(TestData.CATEGORY_ITEM_2)
            self.click(TestData.CATEGORY_ITEM_2)
            time.sleep(5)
            # TelegramReport.send_tg("goods_list_first_good clicked on phone 1")

        with allure.step("Прокрутка до кнопки SUGGEST_GIFT_TO_FRIEND_BUTTON"):
            self.scroll_until_visible(self.driver, MainPage.SUGGEST_GIFT_TO_FRIEND_BUTTON)
            self.is_element_visible(MainPage.SUGGEST_GIFT_TO_FRIEND_BUTTON)
            self.click(MainPage.SUGGEST_GIFT_TO_FRIEND_BUTTON)
            # TelegramReport.send_tg("ADD_TO_WISHES_BUTTON clicked on phone 1")

        with allure.step("Добавление желания без настроек"):
            self.is_element_visible(MainPage.SUGGEST_BUTTON)
            self.click(MainPage.SUGGEST_BUTTON)
            self.is_element_visible(MainPage.NOTIFICATION_WISH_SUGGESTED_TO_FRIEND)
            self.is_element_invisible(MainPage.NOTIFICATION_WISH_SUGGESTED_TO_FRIEND)
            time.sleep(1)

    def accept_first_wish_privacy_all(self):
        # Добавление желания
        with allure.step("Нажатие кнопки нижнего меню каталога"):
            time.sleep(1)
            self.is_element_visible(TestData.BOTTOM_FRIENDS_BTN_XP)
            self.click(TestData.BOTTOM_FRIENDS_BTN_XP)
            self.is_element_visible(TestData.BOTTOM_WISHES_BTN)
            self.click(TestData.BOTTOM_WISHES_BTN)

            time.sleep(1)
            self.is_element_visible(MainPage.ACCEPT_SUGG_WISH_BUTTON)
            self.click(MainPage.ACCEPT_SUGG_WISH_BUTTON)

            self.is_element_visible(MainPage.ADD_WISH_WITHOUT_SETTINGS)
            self.click(MainPage.ADD_WISH_WITHOUT_SETTINGS)
            time.sleep(1)

    def accept_first_wish_privacy_me(self):
        # Добавление желания
        with allure.step("Нажатие кнопки нижнего меню каталога"):
            time.sleep(1)
            self.click(TestData.BOTTOM_WISHES_BTN)
            # TelegramReport.send_tg("click(MainPage.CATALOG_BOTTOM_BUTTON_BOUNDS)")

        with allure.step("Выбор ACCEPT_WISH_BUTTON"):
            self.is_element_visible(MainPage.ACCEPT_WISH_BUTTON)
            self.click(MainPage.ACCEPT_WISH_BUTTON)
            # TelegramReport.send_tg("CATALOG_CATEGORIES_BUTTON clicked on phone 1")

        with allure.step("Выбор ADD_WISH_WITHOUT_SETTINGS"):
            self.is_element_visible(MainPage.ADD_WISH_WITH_SETTINGS)
            self.click(MainPage.ADD_WISH_WITH_SETTINGS)
            # self.is_element_visible(MainPage.NOTIFICATION_WISH_ADDED)
            time.sleep(2)
            # TelegramReport.send_tg("ADD_WISH_WITH_SETTINGS clicked on phone 1")
            self.click_by_uiautomator_desc_contains(MainPage.PRIVACY_ONLY_ME_DESC)
            time.sleep(2)
            self.click(MainPage.ACCEPT_WISH_BUTTON)

    def accept_two_wish_privacy_all(self):
        # Добавление желания
        with allure.step("Нажатие кнопки нижнего меню каталога"):
            time.sleep(1)
            self.click(TestData.BOTTOM_WISHES_BTN)
            # TelegramReport.send_tg("click(MainPage.CATALOG_BOTTOM_BUTTON_BOUNDS)")

        with allure.step("Выбор ACCEPT_WISH_BUTTON"):
            self.is_element_visible(MainPage.ACCEPT_1_WISH_BUTTON)
            self.click(MainPage.ACCEPT_1_WISH_BUTTON)
            # TelegramReport.send_tg("CATALOG_CATEGORIES_BUTTON clicked on phone 1")

        with allure.step("Выбор ADD_WISH_WITHOUT_SETTINGS"):
            self.is_element_visible(MainPage.ACCEPT_WISH_BUTTON)
            self.click(MainPage.ACCEPT_WISH_BUTTON)
            # self.is_element_visible(MainPage.NOTIFICATION_WISH_ADDED)
            time.sleep(1)

        with allure.step("Выбор ACCEPT_WISH_BUTTON"):
            self.is_element_visible(MainPage.ACCEPT_1_WISH_BUTTON)
            self.click(MainPage.ACCEPT_1_WISH_BUTTON)
            # TelegramReport.send_tg("CATALOG_CATEGORIES_BUTTON clicked on phone 1")

        with allure.step("Выбор ADD_WISH_WITHOUT_SETTINGS"):
            self.is_element_visible(MainPage.ACCEPT_WISH_BUTTON)
            self.click(MainPage.ACCEPT_WISH_BUTTON)
            # self.is_element_visible(MainPage.NOTIFICATION_WISH_ADDED)
            time.sleep(1)

    def upload_image_to_device(driver, relative_image_path, device_image_path):
        # Поднимаемся до корня проекта
        project_root = Path(__file__).resolve().parents[2]
        full_image_path = project_root / relative_image_path

        if not full_image_path.exists():
            raise FileNotFoundError(f"Файл не найден: {full_image_path}")

        with full_image_path.open("rb") as file:
            encoded_file = base64.b64encode(file.read()).decode("utf-8")

        if hasattr(driver, "driver"):
            driver.driver.push_file(device_image_path, encoded_file)
        else:
            raise AttributeError("Объект не имеет доступа к Appium-драйверу")

    def add_one_wish(self):
        # Добавление желания
        time.sleep(2)
        self.is_element_visible(TestData.BOTTOM_CATALOG_BTN)
        self.click(TestData.BOTTOM_CATALOG_BTN)
        time.sleep(5)
        self.is_element_visible(TestData.CATALOG_CATEGORIES_BTN)
        self.click(TestData.CATALOG_CATEGORIES_BTN)
        time.sleep(2)
        self.is_element_visible_by_resource_id(TestData.CATEGORY_LIST_ITEM_1)
        self.click_by_uiautomator(TestData.CATEGORY_LIST_ITEM_1)
        time.sleep(2)
        self.is_element_visible_by_resource_id(TestData.CATEGORY_ITEM_2)
        self.click_by_uiautomator(TestData.CATEGORY_ITEM_2)
        time.sleep(5)
        self.scroll_until_visible(self.driver, MainPage.ADD_TO_WISHES_BUTTON)
        time.sleep(3)
        self.click(MainPage.ADD_TO_WISHES_BUTTON)
        time.sleep(5)
        self.click(MainPage.ADD_WISH_WITHOUT_SETTINGS)
        time.sleep(2)

    def click_element_podrobnee(self):
        first_button = self.driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Подробнее").instance(0)'
        )
        first_button.click()

        pass

    def add_custom_wish(self, link):
        self.is_element_visible(TestData.BOTTOM_WISHES_BTN)
        self.click(TestData.BOTTOM_WISHES_BTN)
        self.is_element_visible(MainPage.ADD_WISH_BUTTON)
        self.click(MainPage.ADD_WISH_BUTTON)
        self.is_element_visible(TestData.custom_wish_add_button)
        self.click(TestData.custom_wish_add_button)
        self.is_element_visible(MainPage.ADD_CUSTOM_WISH_LINK)
        self.click(MainPage.ADD_CUSTOM_WISH_LINK)
        self.send_keys(MainPage.ADD_CUSTOM_WISH_LINK, link)
        self.click(TestData.next_button)
        if self.is_element_visible(TestData.BRO_WAIT):
            self.is_element_invisible(TestData.BRO_WAIT)
            self.is_element_visible(TestData.next_button)
            self.click(TestData.next_button)
            self.is_element_visible(TestData.next_button)
            self.click(TestData.next_button)
        else:
            self.is_element_visible(TestData.next_button)
            self.click(TestData.next_button)
            self.is_element_visible(TestData.next_button)
            self.click(TestData.next_button)
        pass

    def exc_handle(self, test_name_this, report_url, e, ):
        # Полный traceback в строку
        full_trace = traceback.format_exc()
        # Фильтрация traceback для оставления только ключевых строк
        trace_lines = []
        for line in full_trace.split('\n'):
            # Оставляем строки с файлами тестов или страниц, и строки с вызовами методов
            if any(keyword in line for keyword in
                   ['test_', 'page.py', ' until(', ' until(']) or line.strip().startswith('File "'):
                trace_lines.append(line)
        # Берем только первые 5 ключевых строк (можно регулировать количество)
        filtered_trace = '\n'.join(trace_lines[:5])
        error_msg = (
            f"❌ <b>Тест упал:</b> {test_name_this}\n"
            f"<b>Ошибка:</b> {type(e).__name__}:\n"
            f"📌<code>{filtered_trace}</code>\n"
            f"🔗 {TelegramReport.format_link('Отчёт', report_url) if report_url != 'недоступен' else 'Отчёт недоступен'}"
        )
        #TelegramReport.send_tg(error_msg)

    def exit_app_and_reopen(self):
        time.sleep(1)
        self.driver.press_keycode(4)
        time.sleep(1)

        self.is_element_visible(TestData.exit_confirm_button)
        self.click(TestData.exit_confirm_button)
        # TelegramReport.send_tg("exit_confirm_button")
        time.sleep(1)

        package = "ru.e2e_test_proj.dev"
        activity = "ru.e2e_test_proj.dev.MainActivity"

        self.driver.activate_app(package)
        # TelegramReport.send_tg("activate_app")
        time.sleep(10)

    def open_add_contact_screen(self):
        """
        Открывает системное окно добавления нового контакта через системный интент и добавляет контакт Vtoroy.
        """
        self.driver.execute_script("mobile: shell", {
            "command": "am",
            "args": [
                "start",
                "-a", "android.intent.action.INSERT",
                "-t", "vnd.android.cursor.dir/contact"
            ],
            "timeout": 5000
        })
        time.sleep(2)

        # Выбираем "Device"
        self.driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().textContains("Device")'
        ).click()
        time.sleep(1)

        # Вводим имя
        first_name_locator = 'new UiSelector().textContains("First name")'
        self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, first_name_locator).send_keys("Vtoroy")
        time.sleep(1)

        # Вводим номер телефона (с очисткой)
        edit_texts = self.driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText")
        if len(edit_texts) < 4:
            raise Exception("Ожидалось минимум 4 поля ввода, но найдено меньше")

        # Четвёртое поле — телефон
        phone_field = edit_texts[3]
        phone_field.clear()
        phone_field.send_keys("+85555555555")

        time.sleep(1)

        # Нажимаем "Save"
        save_button = 'new UiSelector().textContains("Save")'
        self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, save_button).click()

    def exit_app(self):
        time.sleep(2)
        self.driver.press_keycode(4)
        time.sleep(2)

        self.is_element_visible(TestData.exit_confirm_button)
        self.click(TestData.exit_confirm_button)
        time.sleep(1)


    def open_GB_app(self):
        time.sleep(1)

        package = "ru.e2e_test_proj.dev"
        activity = "ru.e2e_test_proj.dev.MainActivity"

        self.driver.activate_app(package)
        # TelegramReport.send_tg("activate_app")
        time.sleep(10)


    def turn_on_gps(self):
        try:
            wait = WebDriverWait(self.driver, 10)
            turn_on_button = wait.until(EC.presence_of_element_located((
                AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Turn on")'
            )))
            turn_on_button.click()
        except Exception as e:
            print(f"Не удалось найти кнопку 'Turn On': {e}")

    def restart_app(self):
        """Безопасный перезапуск приложения e2e_test_proj"""
        try:
            package = "ru.e2e_test_proj.dev"
            # Вариант 1: Через start_activity (предпочтительный)
            self.driver.activate_app(package)
        except Exception as e:
            print(f"Primary restart failed: {e}. Trying fallback methods...")

    def delete_user(self):
        with allure.step("Переход в настройки профиля"):
            self.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR)
            self.click_by_uiautomator(MainPage.PROFILE_SETTINGS_LOCATOR)
            time.sleep(5)
        with allure.step("Прокрутка страницы вверх"):
            self.swipe_up(1600)
            # TelegramReport.send_tg("swipe_up(600)")
            time.sleep(1)
        with allure.step("Выбор личных данных"):
            self.click(TestData.personal_data_bonds)
            time.sleep(1)
        with allure.step("Нажатие на кнопку удаления профиля"):
            self.click(TestData.profile_delete_profile_bonds)
            time.sleep(1)
        with allure.step("Подтверждение удаления профиля"):
            self.click(TestData.profile_delete_confirm_bonds)
            time.sleep(5)
