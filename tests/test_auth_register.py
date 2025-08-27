import logging
import re
import time
import traceback

import allure
import pytest

from ResultCollector import ResultCollector
from core.pages.main_page import MainPage
from core.data.test_data import TestData
from reporting.TelegramReport import TelegramReport
from core.pages.base_test import BaseTest
from core.api.AuthController import AuthController


class AuthRegister(BaseTest):

    @pytest.mark.regress
    @pytest.mark.auth_register_tests
    def test_demo_user_path(self):
        status = "🟡"
        bug_link = "/-/issues/3213"
        test_name_this = "Сценарий демо пути"
        main_page_1 = MainPage(self.driver)
        start_time = time.time()
        collector = ResultCollector()
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")

        try:
            main_page_1.skip_onboarding()

            main_page_1.is_element_visible(TestData.SKIP_BUTTON)
            main_page_1.click(TestData.SKIP_BUTTON)

            main_page_1.is_element_visible(TestData.CATALOG_CATEGORIES_BTN)
            main_page_1.click(TestData.CATALOG_CATEGORIES_BTN)
            time.sleep(5)
            main_page_1.is_element_visible(TestData.CATEGORY_LIST_ITEM_1)
            main_page_1.click(TestData.CATEGORY_LIST_ITEM_1)
            time.sleep(5)
            main_page_1.is_element_visible_by_resource_id(TestData.CATEGORY_ITEM_1)
            main_page_1.click_by_uiautomator(TestData.CATEGORY_ITEM_1)
            time.sleep(5)
            main_page_1.is_element_visible(TestData.BS_AUTH_TO_PROCEED)
            self.driver.back()
            time.sleep(5)
            main_page_1.scroll_until_visible(self.driver, MainPage.SUGGEST_WISH_TO_FRIEND)
            main_page_1.click(MainPage.SUGGEST_WISH_TO_FRIEND)
            main_page_1.is_element_visible(TestData.BS_AUTH_TO_PROCEED)
            self.driver.back()

            main_page_1.is_element_visible(TestData.BOTTOM_HOME_BTN_XP)
            main_page_1.click(TestData.BOTTOM_HOME_BTN_XP)
            main_page_1.is_element_visible(TestData.BS_AUTH_TO_PROCEED)
            self.driver.back()

            main_page_1.is_element_visible(TestData.BOTTOM_FRIENDS_BTN_XP)
            main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
            main_page_1.is_element_visible(TestData.BS_AUTH_TO_PROCEED)
            self.driver.back()

            main_page_1.is_element_visible(TestData.BOTTOM_WISHES_BTN)
            main_page_1.click(TestData.BOTTOM_WISHES_BTN)
            main_page_1.is_element_visible(TestData.BS_AUTH_TO_PROCEED)
            main_page_1.click(TestData.BS_AUTH_TO_PROCEED)


            # Попытка зарегаться после просмотра демо режима
            auth_controller = AuthController()
            auth_controller.authenticate_and_delete_user(TestData.phone_friend1)

            main_page_1.auth_by_phone(TestData.phone_friend1, TestData.confirm_code)
            main_page_1.register_new_user_all_fields(self.driver, "Firsty", "Petrov", "e2e_test_proj@proton.me")
            main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR)
            main_page_1.click_by_uiautomator(MainPage.PROFILE_SETTINGS_LOCATOR)
            time.sleep(5)
            main_page_1.is_element_visible(TestData.USER_PROFILE_PHONENUMBER)

            status = "🟢"
        except Exception as e:
            status = "🟡"
            duration = time.time() - start_time
            main_page_1.exc_handle(test_name_this, report_url, e)
            collector.add_result(test_name_this, status, report_url, duration, bug_link)
            raise
        finally:
            duration = time.time() - start_time
            collector.add_result(test_name_this, status, report_url, duration, bug_link)
    
    
    @pytest.mark.regress
    @pytest.mark.auth_register_tests
    def test_register_and_auth_new_user_all_fields(self):
        """Регистрация пользователя все поля заполняются + Авторизация пользователя с заполненными всеми полями при регистрации"""

        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_ss_name = "test_register_and_auth_new_user_all_fields"
        test_name_this = "Регистрация нового пользователя и авторизация с заполненными всеми полями"
        main_page_1 = MainPage(self.driver)
        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        # Authenticate and delete users before the test
        auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        status = "🔴"  # Инициализация переменной
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")

        try:
            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)
            main_page_1.register_new_user_all_fields(self.driver, "Firsty", "Petrov", "e2e_test_proj@proton.me")

            main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR)
            main_page_1.click_by_uiautomator(MainPage.PROFILE_SETTINGS_LOCATOR)
            time.sleep(5)
            main_page_1.is_element_visible(TestData.USER_PROFILE_PHONENUMBER)

            status = "🟢"
        except Exception as e:
            status = ""
            duration = time.time() - start_time
            main_page_1.exc_handle(test_name_this, report_url, e)
            collector.add_result(test_name_this, status, report_url, duration)
            raise
        finally:
            duration = time.time() - start_time
            collector.add_result(test_name_this, status, report_url, duration)

    @pytest.mark.regress
    @pytest.mark.auth_register_tests
    def test_register_negative_5_let(self):
        """Негативные сценарии регистрации, 5 лет
        BUG: /-/issues/3330"""

        #status = "🔴"
        status = "🟡"
        bug_link = "/-/issues/3330"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_ss_name = "test_register_and_auth_5_let"
        test_name_this = "Авторизация & Регистрация: Негативные сценарии регистрации, 5 лет"
        main_page_1 = MainPage(self.driver)
        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        # Authenticate and delete users before the test
        auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        # auth_controller.authenticate_and_register_user(TestData.phone_friend1, TestData.friend1_name, "11", "1111")

        try:
            # Auth
            time.sleep(5)
            with allure.step("Нажатие на поле ввода номера телефона"):
                main_page_1.skip_onboarding()
                main_page_1.is_element_visible(TestData.AUTH_PHONE_FIELD)
                main_page_1.click(TestData.AUTH_PHONE_FIELD)
            time.sleep(2)

            with allure.step("Ввод номера телефона"):
                main_page_1.send_keys_simple(TestData.phone_friend1)
                time.sleep(1)
                self.driver.hide_keyboard()
            time.sleep(2)

            with allure.step("Нажатие на кнопку продолжить"):
                main_page_1.click(MainPage.CONTINUE_BUTTON_LOCATOR)
            time.sleep(2)

            with allure.step("Ввод кода подтверждения"):
                main_page_1.send_keys_simple("1111")
                time.sleep(1)
                self.driver.hide_keyboard()
            time.sleep(2)

            with allure.step("Нажатие на кнопку продолжить"):
                main_page_1.click(MainPage.CONTINUE_BUTTON_LOCATOR)
            # TelegramReport.send_tg(f"click({MainPage.CONTINUE_BUTTON_LOCATOR})")
            time.sleep(2)

            with allure.step("Выбор согласия с условиями"):
                main_page_1.click(TestData.AUTH_CBX_TERMS)
            # TelegramReport.send_tg(f"click(TestData.AUTH_CBX_TERMS)")
            time.sleep(2)

            with allure.step("Нажатие на кнопку продолжить"):
                main_page_1.click(MainPage.CONTINUE_BUTTON_LOCATOR)
            time.sleep(2)

            with allure.step("Ввод имени пользователя"):
                main_page_1.click(TestData.register_name)
            # TelegramReport.send_tg(f"click(TestData.register_name)")
            time.sleep(2)
            main_page_1.send_keys_simple("mnene5let")
            time.sleep(1)
            self.driver.hide_keyboard()

            with allure.step("Выбор даты рождения"):
                main_page_1.click_by_uiautomator(TestData.register_bday)
            time.sleep(2)
            # TelegramReport.send_tg(f"click_by_uiautomator(TestData.register_bday)")
            main_page_1.send_keys_simple("11112024")
            time.sleep(1)
            self.driver.hide_keyboard()

            with allure.step("Прокрутка до кнопки продолжить"):
                main_page_1.scroll_until_visible(self.driver, MainPage.CONTINUE_BUTTON_LOCATOR)
            time.sleep(2)

            with allure.step("Нажатие на кнопку продолжить"):
                main_page_1.click(MainPage.CONTINUE_BUTTON_LOCATOR)

            with allure.step("Проверка отображения уведомления о возрасте 5 лет"):
                self.assertTrue(
                    main_page_1.is_element_visible(MainPage.NOTIFICATION_5_YEARS),
                    "NOTIFICATION_FIREND_ADDED_WISH не отображается!"
                )
                self.assertTrue(
                    main_page_1.is_element_invisible(MainPage.NOTIFICATION_5_YEARS),
                    "NOTIFICATION_FIREND_ADDED_WISH не скрывается!"
                )
                # TelegramReport.send_tg("NOTIFICATION_FIREND_ADDED_WISH visible main_page_1")

            status = "🟢"
        except Exception as e:
            #status = "🔴"
            status = "🟡"
            duration = time.time() - start_time
            main_page_1.exc_handle(test_name_this, report_url, e)
            collector.add_result(test_name_this, status, report_url, duration, bug_link)
            raise
        finally:
            duration = time.time() - start_time
            collector.add_result(test_name_this, status, report_url, duration, bug_link)

    @pytest.mark.regress
    @pytest.mark.auth_register_tests
    def test_register_negative_fields(self):
        """Регистрация пользователя проверка обязательности заполнения дня рождения при регистрации
            Регистрация пользователя проверка заполнения данных в профиле кроме фамилии
            Авторизация пользователя проверка если в профиле нет фамилии
            Регистрация пользователя проверка заполнения данных в профиле кроме имени"""

        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_ss_name = "test_register_negative_fields"
        test_name_this = "Авторизация & Регистрация: Негативные сценарии регистрации, проверка обязательности заполнения данных"
        main_page_1 = MainPage(self.driver)
        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        # Authenticate and delete users before the test
        auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        # auth_controller.authenticate_and_register_user(TestData.phone_friend1, TestData.friend1_name, "11", "1111")

        try:
            # Auth
            time.sleep(20)
            with allure.step("Нажатие на поле ввода номера телефона"):
                main_page_1.skip_onboarding()
                main_page_1.is_element_visible(TestData.AUTH_PHONE_FIELD)
                main_page_1.click(TestData.AUTH_PHONE_FIELD)
            time.sleep(2)

            with allure.step("Ввод номера телефона"):
                main_page_1.send_keys_simple(TestData.phone_friend1)
            self.driver.hide_keyboard()
            time.sleep(2)

            with allure.step("Нажатие на кнопку продолжить"):
                main_page_1.scroll_until_visible(self.driver, MainPage.CONTINUE_BUTTON_LOCATOR)
                time.sleep(2)
                main_page_1.click(MainPage.CONTINUE_BUTTON_LOCATOR)
            time.sleep(2)

            with allure.step("Ввод кода подтверждения"):
                main_page_1.send_keys_simple("1111")
            time.sleep(2)
            self.driver.hide_keyboard()

            with allure.step("Нажатие на кнопку продолжить"):
                main_page_1.scroll_until_visible(self.driver, MainPage.CONTINUE_BUTTON_LOCATOR)
                time.sleep(2)
                main_page_1.click(MainPage.CONTINUE_BUTTON_LOCATOR)
            # TelegramReport.send_tg(f"click({MainPage.CONTINUE_BUTTON_LOCATOR})")
            time.sleep(2)

            with allure.step("Выбор согласия с условиями"):
                main_page_1.click(TestData.AUTH_CBX_TERMS)
            # TelegramReport.send_tg(f"click(TestData.AUTH_CBX_TERMS)")
            time.sleep(2)

            with allure.step("Нажатие на кнопку продолжить"):
                main_page_1.scroll_until_visible(self.driver, MainPage.CONTINUE_BUTTON_LOCATOR)
                time.sleep(2)
                main_page_1.click(MainPage.CONTINUE_BUTTON_LOCATOR)
            time.sleep(3)

            with allure.step("1 Нажатие на кнопку продолжить"):
                main_page_1.scroll_until_visible(self.driver, MainPage.CONTINUE_BUTTON_LOCATOR)
                time.sleep(2)
                main_page_1.click(MainPage.CONTINUE_BUTTON_LOCATOR)
                main_page_1.is_element_visible(TestData.FIELD_CANNOT_BE_EMPTY_1)
                main_page_1.is_element_visible(TestData.FIELD_CANNOT_BE_EMPTY_2)
            time.sleep(2)

            with allure.step("Ввод имени пользователя"):
                main_page_1.click(TestData.register_name)
                # TelegramReport.send_tg(f"click(TestData.register_name)")
                time.sleep(2)
                main_page_1.send_keys_simple("Pervy")
                self.driver.hide_keyboard()
                time.sleep(2)

            with allure.step("Нажатие на кнопку продолжить"):
                main_page_1.scroll_until_visible(self.driver, MainPage.CONTINUE_BUTTON_LOCATOR)
                time.sleep(2)
                main_page_1.click(MainPage.CONTINUE_BUTTON_LOCATOR)
            time.sleep(2)

            with allure.step("Очистка имени пользователя"):
                main_page_1.click(TestData.register_name)
                main_page_1.clear_text_field_simple(self.driver)
                self.driver.hide_keyboard()
                time.sleep(2)

            with allure.step("Выбор даты рождения"):
                main_page_1.click_by_uiautomator(TestData.register_bday)
            time.sleep(2)
            # TelegramReport.send_tg(f"click_by_uiautomator(TestData.register_bday)")
            main_page_1.send_keys_simple("11112024")
            self.driver.hide_keyboard()
            time.sleep(2)

            with allure.step("Нажатие на кнопку продолжить"):
                main_page_1.scroll_until_visible(self.driver, MainPage.CONTINUE_BUTTON_LOCATOR)
                time.sleep(2)
                main_page_1.click(MainPage.CONTINUE_BUTTON_LOCATOR)
            time.sleep(2)

            status = "🟢"
        except Exception as e:
            status = "🔴"
            duration = time.time() - start_time
            main_page_1.exc_handle(test_name_this, report_url, e)
            collector.add_result(test_name_this, status, report_url, duration)
            raise
        finally:
            duration = time.time() - start_time
            collector.add_result(test_name_this, status, report_url, duration)
