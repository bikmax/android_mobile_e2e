import logging
import time
import traceback
import re

import allure
import pytest

from ResultCollector import ResultCollector
from core.pages.main_page import MainPage
from core.data.test_data import TestData
from reporting.TelegramReport import TelegramReport
from core.pages.base_test import BaseTest
from core.api.AuthController import AuthController

"""
Run tests: python tests/runner.py suggest_wish_tests
"""


class SuggestWish(BaseTest):

    @pytest.mark.regress
    @pytest.mark.suggest_wish_tests
    def test_suggest_gift_to_friend_and_accept_privacy_all(self):
        """Предложение подарка другу, принятие подарка другом с приватностью ВСЕМ"""
        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = "Предложение Желания: другу, принятие подарка другом(через мои желания) с приватностью ВСЕМ"
        test_ss_name = "test_suggest_gift_to_friend_and_accept_privacy_all"
        main_page_1 = MainPage(self.driver)

        auth_controller = AuthController()
        start_time = time.time()
        start_time = time.time()
        collector = ResultCollector()

        # Authenticate and delete users before the test
        auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend2)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend3)
        auth_controller.authenticate_and_register_user(TestData.phone_friend1, "Firsty", "11", "1111")
        auth_controller.authenticate_and_register_user(TestData.phone_friend2, "Vtoroy", "12", "1111")
        auth_controller.authenticate_and_register_user(TestData.phone_friend3, "Treti", "13", "1111")

        try:
            # Auth
            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)

            main_page_1.suggest_wish_to_friend_1()

            main_page_1.logout(self.driver)

            main_page_1.auth_by_phone(TestData.phone_friend3, TestData.confirm_code)

            time.sleep(5)
            main_page_1.accept_first_wish_privacy_all()

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

    @pytest.mark.regress
    @pytest.mark.suggest_wish_tests
    @allure.story("Предложение подарка другу и принятие с приватностью Только мне")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_suggest_gift_to_friend_and_accept_privacy_onlyme(self):
        """Предложение подарка другу, принятие подарка другом с приватностью Только мне"""
        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = "Предложение подарка другу и принятие с приватностью Только мне"
        test_ss_name = "test_suggest_gift_to_friend_and_accept_privacy_onlyme"
        main_page_1 = MainPage(self.driver)

        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        # Authenticate and delete users before the test
        auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend2)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend3)
        auth_controller.authenticate_and_register_user(TestData.phone_friend1, "Firsty", "11", "1111")
        auth_controller.authenticate_and_register_user(TestData.phone_friend2, "Vtoroy", "12", "1111")
        auth_controller.authenticate_and_register_user(TestData.phone_friend3, "Treti", "13", "1111")

        try:
            # Auth
            time.sleep(20)
            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)
            time.sleep(2)


            # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")

            # Refresh contacts
            time.sleep(2)
            with allure.step("Обновление контактов на телефоне 1"):
                main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
                time.sleep(2)
                main_page_1.swipe_down(1999)
                time.sleep(2)

            time.sleep(2)
            with allure.step("Обновление контактов на телефоне 2"):
                main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
                time.sleep(2)
                main_page_1.swipe_down(1999)
                time.sleep(2)

            # Start phone 1
            time.sleep(2)
            with allure.step("Выбор первого друга на телефоне 1"):
                main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
                # TelegramReport.send_tg("click(TestData.first_friend_bonds)")
                time.sleep(2)
                main_page_1.scroll_until_visible(self.driver, MainPage.SUGGEST_WISH_TO_FRIEND)
                time.sleep(2)
                main_page_1.click(MainPage.SUGGEST_WISH_TO_FRIEND)
                # TelegramReport.send_tg("click(MainPage.SUGGEST_WISH_TO_FRIEND)")
                time.sleep(2)
                main_page_1.click(MainPage.CHOOSE_FROM_CATALOG_BUTTON)
                # TelegramReport.send_tg("click(MainPage.CHOOSE_FROM_CATALOG_BUTTON)")
                time.sleep(2)
                main_page_1.click(TestData.CATALOG_CATEGORIES_BTN)
                # TelegramReport.send_tg("CATALOG_CATEGORIES_BUTTON clicked on phone 1")
                time.sleep(2)
                main_page_1.click_by_uiautomator(TestData.CATEGORY_LIST_ITEM_1)
                # TelegramReport.send_tg("CATALOG_LIGHT_BUTTON clicked on phone 1")
                time.sleep(2)
                main_page_1.click(TestData.CATEGORY_ITEM_2)
                # TelegramReport.send_tg("catalog_first_good clicked on phone 1")
                time.sleep(5)
                main_page_1.scroll_until_visible(self.driver, MainPage.SUGGEST_GIFT_TO_FRIEND_BUTTON)
                time.sleep(2)
                main_page_1.click(MainPage.SUGGEST_GIFT_TO_FRIEND_BUTTON)
                # TelegramReport.send_tg("SUGGEST_GIFT_TO_FRIEND_BUTTON clicked on phone 1")
                time.sleep(2)
                main_page_1.click(MainPage.SUGGEST_BUTTON)
                # TelegramReport.send_tg("ADD_TO_WISHES_BUTTON clicked on phone 1")

            # Start phone 2 accept privacy only me
            with allure.step("Начало выполнения на телефоне 2 с принятием подарка с настройкой 'Только мне'"):
                main_page_1.logout(self.driver)
                main_page_1.auth_by_phone(TestData.phone_friend3, TestData.confirm_code)
                main_page_1.accept_first_wish_privacy_me()

            with allure.step("Проверка что не видно желания"):
                main_page_1.logout(self)
                main_page_1.exit_app_and_reopen()
                main_page_1.auth_by_phone(TestData.phone_friend3, TestData.confirm_code)
                main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
                main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
                time.sleep(5)
                main_page_1.is_element_visible(TestData.friend_wish_first_wish)

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

    @pytest.mark.regress
    @pytest.mark.suggest_wish_tests
    @allure.story("Тестирование предложения подарка другу и принятие подарка с приватностью SOME")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_suggest_gift_to_friend_and_accept_privacy_some_1(self):
        """Предложение подарка другу, принятие подарка другом с приватностью SOME, видимый тому кто предложил"""
        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        main_page_1 = MainPage(self.driver)

        test_name_this = "Предложение желания из каталога и принятие его другом с видимостью для нескольких пользователей, видимый тому кто предложил"
        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()
        test_ss_name = "test_suggest_gift_to_friend_and_accept_privacy_some_1"

        # Authenticate and delete users before the test
        auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend2)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend3)
        auth_controller.authenticate_and_register_user(TestData.phone_friend1, "Firsty", "11", "1111")
        auth_controller.authenticate_and_register_user(TestData.phone_friend2, "Vtoroy", "12", "1111")
        auth_controller.authenticate_and_register_user(TestData.phone_friend3, "Treti", "13", "1111")

        try:
            # Auth
            time.sleep(20)
            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)
            time.sleep(2)


            # Начало телефон 1
            time.sleep(2)
            with allure.step("Нажатие на первого друга"):
                main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
            # TelegramReport.send_tg("click(TestData.first_friend_bonds)")
            time.sleep(2)
            with allure.step("Прокрутка до кнопки предложения подарка"):
                main_page_1.scroll_until_visible(self.driver, MainPage.SUGGEST_WISH_TO_FRIEND)
            time.sleep(2)
            with allure.step("Нажатие на кнопку предложения подарка другу"):
                main_page_1.click(MainPage.SUGGEST_WISH_TO_FRIEND)
            # TelegramReport.send_tg("click(MainPage.SUGGEST_WISH_TO_FRIEND)")
            time.sleep(2)
            with allure.step("Нажатие на кнопку выбора из каталога"):
                main_page_1.click(MainPage.CHOOSE_FROM_CATALOG_BUTTON)
            # TelegramReport.send_tg("click(MainPage.CHOOSE_FROM_CATALOG_BUTTON)")
            time.sleep(2)
            with allure.step("Нажатие на кнопку выбора категории товаров"):
                main_page_1.click(TestData.CATALOG_CATEGORIES_BTN)
            # TelegramReport.send_tg("Категория товаров выбрана на телефоне 1")
            time.sleep(2)
            with allure.step("Нажатие на кнопку выбора товара из категории"):
                main_page_1.click_by_uiautomator(TestData.CATEGORY_LIST_ITEM_1)
            # TelegramReport.send_tg("Выбор товара из категории на телефоне 1")
            time.sleep(2)
            with allure.step("Выбор товара"):
                main_page_1.click(TestData.CATEGORY_ITEM_2)
            # TelegramReport.send_tg("Выбор товара на телефоне 1")
            time.sleep(5)
            with allure.step("Прокрутка до кнопки предложения подарка другу"):
                main_page_1.scroll_until_visible(self.driver, MainPage.SUGGEST_GIFT_TO_FRIEND_BUTTON)
            time.sleep(2)
            with allure.step("Нажатие на кнопку предложения подарка другу"):
                main_page_1.click(MainPage.SUGGEST_GIFT_TO_FRIEND_BUTTON)
            # TelegramReport.send_tg("click(MainPage.SUGGEST_GIFT_TO_FRIEND_BUTTON) на телефоне 1")
            time.sleep(2)
            with allure.step("Нажатие на кнопку выбора первого друга"):
                main_page_1.click_element_by_bounds(TestData.catalog_suggest_wish_first_friend)
            time.sleep(2)
            with allure.step("Нажатие на кнопку добавить подарок в желания"):
                main_page_1.click(MainPage.SUGGEST_WISH_BUTTON)
            # TelegramReport.send_tg("Нажатие на кнопку ADD_TO_WISHES_BUTTON на телефоне 1")

            with allure.step("exit app"):
                main_page_1.logout(self)
                main_page_1.exit_app_and_reopen()
                main_page_1.auth_by_phone(TestData.phone_friend3, TestData.confirm_code)

            # Начало телефон 2, принятие подарка
            with allure.step("Нажатие на кнопку просмотра желаемого на телефоне 2"):
                main_page_1.click(TestData.BOTTOM_WISHES_BTN)
            # TelegramReport.send_tg("click(TestData.BOTTOM_WISHES_BTN) на телефоне 2")
            time.sleep(3)
            with allure.step("Прокрутка вниз на телефоне 2"):
                main_page_1.swipe_up(600)
            time.sleep(2)
            with allure.step("Нажатие на кнопку принятия подарка на телефоне 2"):
                main_page_1.click(MainPage.ACCEPT_WISH_BUTTON)
            # TelegramReport.send_tg("click(MainPage.ACCEPT_WISH_BUTTON) на телефоне 2")
            time.sleep(2)
            with allure.step("Нажатие на кнопку добавления подарка с настройками на телефоне 2"):
                main_page_1.click(MainPage.ADD_WISH_WITH_SETTINGS)
            # TelegramReport.send_tg("click(MainPage.ADD_WISH_WITH_SETTINGS) на телефоне 2")
            time.sleep(2)
            with allure.step("Нажатие на поле описания на телефоне 2"):
                main_page_1.click(MainPage.DESCRIPTION_FILED)
            # TelegramReport.send_tg("click(MainPage.DESCRIPTION_FILED) на телефоне 2")
            time.sleep(2)


            with allure.step("Проверка того что видно подарок"):
                main_page_1.logout(self)
                main_page_1.auth_by_phone(TestData.phone_friend1, TestData.confirm_code)
                main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
                main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
                main_page_1.is_element_visible(TestData.friend_wish_first_wish)

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

    @pytest.mark.regress
    @pytest.mark.suggest_wish_tests
    @allure.story(
        "Тест: Предложение желания из каталога и принятие его другом с видимостью для нескольких пользователей, но не друга предложившего желание")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_suggest_gift_to_friend_and_accept_privacy_some_2(self):
        """Предложение желания из каталога и принятие его другом с видимостью для нескольких юзеров но не друга предложившего желание"""
        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        main_page_1 = MainPage(self.driver)

        test_name_this = "Предложение желания из каталога и принятие его другом с видимостью для нескольких пользователей, но не друга предложившего желание"
        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()
        test_ss_name = "test_suggest_custom_gift_to_friend_and_accept_privacy_some"

        # Authenticate and delete users before the test
        auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend2)
        auth_controller.authenticate_and_register_user(TestData.phone_friend1, "Firsty", "11", "1111")
        auth_controller.authenticate_and_register_user(TestData.phone_friend2, "Vtoroy", "12", "1111")

        try:
            # Auth
            time.sleep(20)
            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)
            time.sleep(2)

            # Startphone 1
            with allure.step("Нажатие на первого друга"):
                time.sleep(2)
                main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
                # TelegramReport.send_tg("click(TestData.first_friend_bonds)")

            with allure.step("Прокрутка и выбор предложения желания"):
                time.sleep(2)
                main_page_1.scroll_until_visible(self.driver, MainPage.SUGGEST_WISH_TO_FRIEND)
                time.sleep(2)
                main_page_1.click(MainPage.SUGGEST_WISH_TO_FRIEND)
                # TelegramReport.send_tg("click(MainPage.SUGGEST_WISH_TO_FRIEND)")
                time.sleep(2)
                main_page_1.click(MainPage.CHOOSE_FROM_CATALOG_BUTTON)
                # TelegramReport.send_tg("click(MainPage.CHOOSE_FROM_CATALOG_BUTTON)")

            with allure.step("Выбор категории товаров и товара"):
                time.sleep(2)
                main_page_1.click(TestData.CATALOG_CATEGORIES_BTN)
                # TelegramReport.send_tg("CATALOG_CATEGORIES_BUTTON clicked on phone 1")
                time.sleep(2)
                main_page_1.click_by_uiautomator(TestData.CATEGORY_LIST_ITEM_1)
                # TelegramReport.send_tg("CATALOG_LIGHT_BUTTON clicked on phone 1")
                time.sleep(2)
                main_page_1.click(TestData.CATEGORY_ITEM_2)
                # TelegramReport.send_tg("catalog_first_good clicked on phone 1")
                time.sleep(5)

            with allure.step("Прокрутка до кнопки предложения подарка"):
                main_page_1.scroll_until_visible(self.driver, MainPage.SUGGEST_GIFT_TO_FRIEND_BUTTON)
                time.sleep(2)
                main_page_1.click(MainPage.SUGGEST_GIFT_TO_FRIEND_BUTTON)
                # TelegramReport.send_tg("SUGGEST_GIFT_TO_FRIEND_BUTTON clicked on phone 1")
                time.sleep(2)
                main_page_1.click_element_by_bounds(TestData.catalog_suggest_wish_first_friend)
                time.sleep(2)
                main_page_1.click(MainPage.SUGGEST_WISH_BUTTON)
                # TelegramReport.send_tg("ADD_TO_WISHES_BUTTON clicked on phone 1")

            main_page_1.logout(self)
            main_page_1.auth_by_phone(TestData.phone_friend3, TestData.confirm_code)

            # Start phone 2, accept privacy only me
            with allure.step("Принятие предложения на телефоне 2"):
                main_page_1.click(TestData.BOTTOM_WISHES_BTN)
                # TelegramReport.send_tg("click(TestData.BOTTOM_WISHES_BTN) called")
                time.sleep(3)
                main_page_1.scroll_until_visible(self.driver, MainPage.ACCEPT_WISH_BUTTON)
                time.sleep(2)
                main_page_1.click(MainPage.ACCEPT_WISH_BUTTON)
                # TelegramReport.send_tg("click(MainPage.ACCEPT_WISH_BUTTON) called")
                time.sleep(2)
                main_page_1.click(MainPage.ADD_WISH_WITH_SETTINGS)
                # TelegramReport.send_tg("click(MainPage.ADD_WISH_WITH_SETTINGS) called")
                time.sleep(2)
                main_page_1.click(MainPage.DESCRIPTION_FILED)
                # TelegramReport.send_tg("click(MainPage.DESCRIPTION_FILED)")

            with allure.step("Проверка того что не видно подарка"):
                main_page_1.logout(self)
                main_page_1.auth_by_phone(TestData.phone_friend1, TestData.confirm_code)
                main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
                main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
                time.sleep(5)
                main_page_1.is_element_invisible(TestData.friend_wish_first_wish)

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

    @pytest.mark.suggest_wish_tests
    def test_suggest_gift_to_friend_and_decline_gift(self):
        """Предложение подарка другу, ОТКЛОНЕНИЕ подарка другом"""
        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = ""
        test_ss_name = "test_suggest_gift_to_friend_and_accept_privacy_all"
        main_page_1 = MainPage(self.driver)

        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        # Authenticate and delete users before the test
        auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend2)
        auth_controller.authenticate_and_register_user(TestData.phone_friend1, "Firsty", "11", "1111")
        auth_controller.authenticate_and_register_user(TestData.phone_friend2, "Vtoroy", "12", "1111")

        try:
            # Auth
            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)

            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend2, TestData.confirm_code)
            main_page_1.register_new_user(self.driver, TestData.phone_friend2)

            self.assertTrue(
                main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                "Profile settings button not visible!"
            )
            # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")

            # Start phone 1 suggest wish
            time.sleep(2)
            main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
            # TelegramReport.send_tg("click(MainPage.FRIENDS_BUTTON)")
            time.sleep(2)
            main_page_1.click_element_by_bounds(TestData.second_friend_bonds)
            # TelegramReport.send_tg("click(TestData.first_friend_bonds)")
            time.sleep(2)
            main_page_1.scroll_until_visible(self.driver, MainPage.SUGGEST_WISH_TO_FRIEND)
            main_page_1.click(MainPage.SUGGEST_WISH_TO_FRIEND)
            # TelegramReport.send_tg("click(MainPage.SUGGEST_WISH_TO_FRIEND)")
            time.sleep(2)
            main_page_1.click(MainPage.CHOOSE_FROM_CATALOG_BUTTON)
            # TelegramReport.send_tg("click(MainPage.CHOOSE_FROM_CATALOG_BUTTON)")
            time.sleep(2)
            main_page_1.click(TestData.CATALOG_CATEGORIES_BTN)
            # TelegramReport.send_tg("CATALOG_CATEGORIES_BUTTON clicked on phone 1")
            time.sleep(2)
            main_page_1.click_by_uiautomator(TestData.CATEGORY_LIST_ITEM_1)
            # TelegramReport.send_tg("CATALOG_LIGHT_BUTTON clicked on phone 1")
            time.sleep(2)
            # main_page_1.click(MainPage.ALL_FROM_CATEGORY)
            # TelegramReport.send_tg("ALL_FROM_CATEGORY clicked on phone 1")
            time.sleep(2)
            main_page_1.click(MainPage.THIRD_GOOD)
            # TelegramReport.send_tg("THIRD_GOOD clicked on phone 1")
            time.sleep(2)
            main_page_1.scroll_until_visible(self.driver, MainPage.SUGGEST_GIFT_TO_FRIEND_BUTTON)
            main_page_1.click(MainPage.SUGGEST_GIFT_TO_FRIEND_BUTTON)
            # TelegramReport.send_tg("SUGGEST_GIFT_TO_FRIEND_BUTTON clicked on phone 1")
            time.sleep(2)
            main_page_1.click(MainPage.SUGGEST_WISH_BUTTON)
            # TelegramReport.send_tg("ADD_TO_WISHES_BUTTON clicked on phone 1")

            # Отклонение

            self.assertTrue(
                main_page_1.is_element_visible(MainPage.NOTIFICATION_WISH_SUGGESTED),
                "NOTIFICATION_WISH_SUGGESTED not visible!"
            )
            self.assertTrue(
                main_page_1.is_element_invisible(MainPage.NOTIFICATION_WISH_SUGGESTED),
                "NOTIFICATION_WISH_SUGGESTED not visible!"
            )

            # Открываем из уведомлений
            main_page_1.click(TestData.notification_bell)
            time.sleep(3)
            main_page_1.click(MainPage.SEE_SUGGESTED_WISH_FROM_NOTIFICATIONS)
            time.sleep(3)

            main_page_1.scroll_until_visible(self.driver, MainPage.DECLINE_WISH_BUTTON)
            main_page_1.click(MainPage.DECLINE_WISH_BUTTON)
            time.sleep(1)
            main_page_1.click_element_by_bounds(TestData.decline_wish_final_button)
            # TelegramReport.send_tg("click(MainPage.ACCEPT_WISH_BUTTON) called")

            self.assertTrue(
                main_page_1.is_element_visible(MainPage.NOTIFICATION_WISH_DECLINED),
                "NOTIFICATION_WISH_SUGGESTED not visible!"
            )
            self.assertTrue(
                main_page_1.is_element_invisible(MainPage.NOTIFICATION_WISH_DECLINED),
                "NOTIFICATION_WISH_SUGGESTED not visible!"
            )
            # TelegramReport.send_tg("NOTIFICATION_WISH_SUGGESTED visible main_page_1")

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

    @pytest.mark.suggest_wish_tests
    @allure.story("Тест: Предложение partner подарка другу, принятие подарка другом с приватностью ВСЕМ")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_suggest_partner_gift_to_friend_and_accept_privacy_all(self):
        """Предложение partner подарка другу, принятие подарка другом с приватностью ВСЕМ"""
        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = ""
        test_ss_name = "test_suggest_partner_gift_to_friend_and_accept_privacy_all"
        main_page_1 = MainPage(self.driver)

        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        # Аутентификация и удаление пользователей перед тестом
        with allure.step("Аутентификация и удаление пользователей перед тестом"):
            auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend2)
        auth_controller.authenticate_and_register_user(TestData.phone_friend1, "Firsty", "11", "1111")
        auth_controller.authenticate_and_register_user(TestData.phone_friend2, "Vtoroy", "12", "1111")

        try:
            # Аутентификация
            with allure.step("Аутентификация пользователей"):
                time.sleep(2)
                main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)
                time.sleep(2)

                time.sleep(2)
                main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend2, TestData.confirm_code)
                time.sleep(2)
                main_page_1.register_new_user(self.driver, TestData.phone_friend2)
                time.sleep(2)

            # Обновление контактов
            with allure.step("Обновление контактов на устройстве 1"):
                time.sleep(2)
                main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
                time.sleep(2)
                main_page_1.swipe_down(1999)
                time.sleep(2)

            with allure.step("Обновление контактов на устройстве 2"):
                time.sleep(2)
                main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
                time.sleep(2)
                main_page_1.swipe_down(1999)
                time.sleep(2)

            # Добавление желания на устройстве 1
            with allure.step("Добавление желания на устройстве 1"):
                time.sleep(2)
                main_page_1.click(TestData.BOTTOM_CATALOG_BTN)
                # TelegramReport.send_tg("click(MainPage.CATALOG_BOTTOM_BUTTON_BOUNDS)")
                time.sleep(5)
                main_page_1.click(TestData.catalog_search_field)
                # TelegramReport.send_tg("CATALOG_CATEGORIES_BUTTON clicked on phone 1")
                time.sleep(2)
                main_page_1.send_keys_simple(TestData.partner_wish)
                time.sleep(2)
                main_page_1.click(TestData.catalog_search_field_result)
                time.sleep(5)
                main_page_1.click_by_uiautomator(TestData.CATEGORY_ITEM_1)
                # TelegramReport.send_tg("goods_list_first_good clicked on phone 1")
                time.sleep(2)
                main_page_1.scroll_until_visible(self.driver, MainPage.SUGGEST_GIFT_TO_FRIEND_BUTTON)
                time.sleep(2)
                main_page_1.click(MainPage.SUGGEST_GIFT_TO_FRIEND_BUTTON)
                # TelegramReport.send_tg("SUGGEST_GIFT_TO_FRIEND_BUTTON clicked on phone 1")
                time.sleep(2)
                main_page_1.click_element_by_bounds(TestData.catalog_suggest_wish_first_friend)
                time.sleep(2)
                main_page_1.click(MainPage.SUGGEST_WISH_BUTTON)
                # TelegramReport.send_tg("ADD_TO_WISHES_BUTTON clicked on phone 1")

            with allure.step("Проверка уведомления о предложении подарка"):
                self.assertTrue(
                    main_page_1.is_element_visible(MainPage.NOTIFICATION_WISH_SUGGESTED_TO_FRIEND),
                    "Уведомление о предложении подарка не видно!"
                )
                self.assertTrue(
                    main_page_1.is_element_invisible(MainPage.NOTIFICATION_WISH_SUGGESTED_TO_FRIEND),
                    "Уведомление о предложении подарка не исчезло!"
                )
                # TelegramReport.send_tg("NOTIFICATION_WISH_SUGGESTED visible main_page_1")

            # Скриншот: после добавления желания на устройстве 1
            action_taken = "_after_wish_add_phone1"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)

            with allure.step("Снимок экрана с эталонным изображением после добавления желания (устройство 1)"):
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
                allure.attach.file(ss_etalon, name="Эталонный скриншот", attachment_type=allure.attachment_type.PNG)

            with allure.step("Снимок экрана с результатом выполнения теста (устройство 1)"):
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
                allure.attach.file(ss_run, name="Скриншот результата", attachment_type=allure.attachment_type.PNG)

            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), "Сравнение изображений не удалось"

            # Принятие желания на устройстве 2
            with allure.step("Принятие желания на устройстве 2"):
                main_page_1.click(TestData.BOTTOM_WISHES_BTN)
                # TelegramReport.send_tg("click(TestData.BOTTOM_WISHES_BTN) called")
                time.sleep(3)
                main_page_1.swipe_up(600)
                time.sleep(2)
                main_page_1.click(MainPage.ACCEPT_WISH_BUTTON)
                # TelegramReport.send_tg("click(MainPage.ACCEPT_WISH_BUTTON) called")

            with allure.step("Настройка принятого желания"):
                main_page_1.click(MainPage.ADD_WISH_WITH_SETTINGS)
                # TelegramReport.send_tg("click(MainPage.ADD_WISH_WITH_SETTINGS) called")
                time.sleep(2)
                main_page_1.click_element_by_bounds(TestData.accept_suggested_wish_desc_field)
                # TelegramReport.send_tg("click(MainPage.DESCRIPTION_FILED) called")
                time.sleep(2)
                main_page_1.send_keys_simple("test gift desc")
                # TelegramReport.send_tg("send_keys(MainPage.DESCRIPTION_FILED, 'test gift desc') called")
                time.sleep(2)
                main_page_1.click_element_by_bounds(MainPage.FINAL_ACCEPT_BONDS)
                # TelegramReport.send_tg("click(MainPage.FINAL_ACCEPT_BONDS) called")
                time.sleep(2)

            with allure.step("Проверка уведомления о добавлении желания"):
                self.assertTrue(
                    main_page_1.is_element_visible(MainPage.NOTIFICATION_WISH_ADDED),
                    "Уведомление о добавлении желания не видно!"
                )
                self.assertTrue(
                    main_page_1.is_element_invisible(MainPage.NOTIFICATION_WISH_ADDED),
                    "Уведомление о добавлении желания не исчезло!"
                )
                # TelegramReport.send_tg("NOTIFICATION_WISH_SUGGESTED visible main_page_1")

            # Скриншот: после принятия желания на устройстве 2
            action_taken = "_after_wish_accept_phone2"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)

            with allure.step("Снимок экрана с эталонным изображением после принятия желания (устройство 2)"):
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
                allure.attach.file(ss_etalon, name="Эталонный скриншот", attachment_type=allure.attachment_type.PNG)

            with allure.step("Снимок экрана с результатом выполнения теста (устройство 2)"):
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
                allure.attach.file(ss_run, name="Скриншот результата", attachment_type=allure.attachment_type.PNG)

            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), "Сравнение изображений не удалось"

            # Проверка видимости подарка на устройстве 1
            with allure.step("Проверка видимости подарка на устройстве 1"):
                main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
                time.sleep(2)
                main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
                # TelegramReport.send_tg("click(TestData.first_friend_bonds)")
                time.sleep(4)

            # Скриншот: проверка видимости подарка на устройстве 1
            action_taken = "_after_wish_accept_visible_phone1"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)

            with allure.step("Снимок экрана с эталонным изображением видимости подарка (устройство 1)"):
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
                allure.attach.file(ss_etalon, name="Эталонный скриншот", attachment_type=allure.attachment_type.PNG)

            with allure.step("Снимок экрана с результатом выполнения теста (видимость подарка, устройство 1)"):
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
                allure.attach.file(ss_run, name="Скриншот результата", attachment_type=allure.attachment_type.PNG)

            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), "Сравнение изображений не удалось"

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

    @pytest.mark.suggest_wish_tests
    @allure.story("Тест: Предложение partner подарка другу, принятие подарка другом с приватностью Только мне")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_suggest_partner_gift_to_friend_and_accept_privacy_onlyme(self):
        """Предложение partner подарка другу, принятие подарка другом с приватностью Только мне"""
        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = ""
        test_ss_name = "test_suggest_partner_gift_to_friend_and_accept_privacy_onlyme"
        main_page_1 = MainPage(self.driver)

        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        # Аутентификация и удаление пользователей перед тестом
        with allure.step("Аутентификация и удаление пользователей перед тестом"):
            auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend2)
        auth_controller.authenticate_and_register_user(TestData.phone_friend1, "Firsty", "11", "1111")
        auth_controller.authenticate_and_register_user(TestData.phone_friend2, "Vtoroy", "12", "1111")

        try:
            # Аутентификация
            with allure.step("Аутентификация пользователей"):
                time.sleep(2)
                main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)
                time.sleep(2)

                time.sleep(2)
                main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend2, TestData.confirm_code)
                time.sleep(2)
                main_page_1.register_new_user(self.driver, TestData.phone_friend2)
                time.sleep(2)

            with allure.step("Проверка видимости кнопки настроек профиля"):
                self.assertTrue(
                    main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                    "Кнопка настроек профиля не видна!"
                )
                # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")

            # Обновление контактов
            with allure.step("Обновление контактов на устройстве 1"):
                time.sleep(2)
                main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
                time.sleep(2)
                main_page_1.swipe_down(1999)
                time.sleep(2)

            with allure.step("Обновление контактов на устройстве 2"):
                time.sleep(2)
                main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
                time.sleep(2)
                main_page_1.swipe_down(1999)
                time.sleep(2)

            # Добавление желания на устройстве 1
            with allure.step("Добавление желания на устройстве 1"):
                time.sleep(2)
                main_page_1.click(TestData.BOTTOM_CATALOG_BTN)
                # TelegramReport.send_tg("click(MainPage.CATALOG_BOTTOM_BUTTON_BOUNDS)")
                time.sleep(5)
                main_page_1.click(TestData.catalog_search_field)
                # TelegramReport.send_tg("CATALOG_CATEGORIES_BUTTON clicked on phone 1")
                time.sleep(2)
                main_page_1.send_keys_simple(TestData.partner_wish)
                time.sleep(2)
                main_page_1.click(TestData.catalog_search_field_result)
                time.sleep(5)
                main_page_1.click_by_uiautomator(TestData.CATEGORY_ITEM_1)
                # TelegramReport.send_tg("goods_list_first_good clicked on phone 1")
                time.sleep(2)
                main_page_1.scroll_until_visible(self.driver, MainPage.SUGGEST_GIFT_TO_FRIEND_BUTTON)
                time.sleep(2)
                main_page_1.click(MainPage.SUGGEST_GIFT_TO_FRIEND_BUTTON)
                # TelegramReport.send_tg("SUGGEST_GIFT_TO_FRIEND_BUTTON clicked on phone 1")
                time.sleep(2)
                main_page_1.click_element_by_bounds(TestData.catalog_suggest_wish_first_friend)
                time.sleep(2)
                main_page_1.click(MainPage.SUGGEST_WISH_BUTTON)
                # TelegramReport.send_tg("ADD_TO_WISHES_BUTTON clicked on phone 1")

            with allure.step("Проверка уведомления о предложении подарка"):
                self.assertTrue(
                    main_page_1.is_element_visible(MainPage.NOTIFICATION_WISH_SUGGESTED_TO_FRIEND),
                    "Уведомление о предложении подарка не видно!"
                )
                self.assertTrue(
                    main_page_1.is_element_invisible(MainPage.NOTIFICATION_WISH_SUGGESTED_TO_FRIEND),
                    "Уведомление о предложении подарка не исчезло!"
                )
                # TelegramReport.send_tg("NOTIFICATION_WISH_SUGGESTED visible main_page_1")

            # Скриншот: после добавления желания на устройстве 1
            action_taken = "_after_wish_add_phone1"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)

            with allure.step("Снимок экрана с эталонным изображением после добавления желания (устройство 1)"):
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
                allure.attach.file(ss_etalon, name="Эталонный скриншот", attachment_type=allure.attachment_type.PNG)

            with allure.step("Снимок экрана с результатом выполнения теста (устройство 1)"):
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
                allure.attach.file(ss_run, name="Скриншот результата", attachment_type=allure.attachment_type.PNG)

            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), "Сравнение изображений не удалось"

            # Принятие желания на устройстве 2
            with allure.step("Принятие желания на устройстве 2"):
                main_page_1.click(TestData.BOTTOM_WISHES_BTN)
                # TelegramReport.send_tg("click(TestData.BOTTOM_WISHES_BTN) called")
                time.sleep(3)
                main_page_1.swipe_up(600)
                time.sleep(2)
                main_page_1.click(MainPage.ACCEPT_WISH_BUTTON)
                # TelegramReport.send_tg("click(MainPage.ACCEPT_WISH_BUTTON) called")

            with allure.step("Настройка принятого желания"):
                time.sleep(2)
                main_page_1.click(MainPage.ADD_WISH_WITH_SETTINGS)
                # TelegramReport.send_tg("click(MainPage.ADD_WISH_WITH_SETTINGS) called")
                time.sleep(2)
                main_page_1.click_element_by_bounds(TestData.accept_suggested_wish_desc_field)
                # TelegramReport.send_tg("click(MainPage.DESCRIPTION_FILED) called")
                time.sleep(2)
                main_page_1.send_keys_simple("test gift desc")
                # TelegramReport.send_tg("send_keys(MainPage.DESCRIPTION_FILED, 'test gift desc') called")
                time.sleep(2)
                main_page_1.scroll_down(self.driver, 1)
                # TelegramReport.send_tg("scroll_down 1")
                time.sleep(2)
                main_page_1.click_element_by_bounds(TestData.suggested_partner_wish_privacy_only_me)
                # TelegramReport.send_tg("click(MainPage.PRIVACY_ONLY_ME_BOUNDS) called")
                time.sleep(2)
                main_page_1.click_element_by_bounds(MainPage.FINAL_ACCEPT_BONDS)
                # TelegramReport.send_tg("click(MainPage.FINAL_ACCEPT_BONDS) called")

            with allure.step("Проверка уведомления о добавлении желания"):
                self.assertTrue(
                    main_page_1.is_element_visible(MainPage.NOTIFICATION_WISH_ADDED),
                    "Уведомление о добавлении желания не видно!"
                )
                # TelegramReport.send_tg("NOTIFICATION_WISH_SUGGESTED visible main_page_1")

            # Скриншот: после принятия желания на устройстве 2
            action_taken = "_after_wish_accept_phone2"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)

            with allure.step("Снимок экрана с эталонным изображением после принятия желания (устройство 2)"):
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
                allure.attach.file(ss_etalon, name="Эталонный скриншот", attachment_type=allure.attachment_type.PNG)

            with allure.step("Снимок экрана с результатом выполнения теста (устройство 2)"):
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
                allure.attach.file(ss_run, name="Скриншот результата", attachment_type=allure.attachment_type.PNG)

            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), "Сравнение изображений не удалось"

            # Проверка видимости подарка на устройстве 1
            with allure.step("Проверка видимости подарка на устройстве 1"):
                main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
                time.sleep(2)
                main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
                # TelegramReport.send_tg("click(TestData.first_friend_bonds)")
                time.sleep(4)

            # Скриншот: проверка видимости подарка на устройстве 1
            action_taken = "_after_wish_accept_visible_phone1"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)

            with allure.step("Снимок экрана с эталонным изображением видимости подарка (устройство 1)"):
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
                allure.attach.file(ss_etalon, name="Эталонный скриншот", attachment_type=allure.attachment_type.PNG)

            with allure.step("Снимок экрана с результатом выполнения теста (видимость подарка, устройство 1)"):
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
                allure.attach.file(ss_run, name="Скриншот результата", attachment_type=allure.attachment_type.PNG)

            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), "Сравнение изображений не удалось"

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

    @pytest.mark.suggest_wish_tests
    @allure.story(
        "Тест: Предложение partner подарка другу, принятие подарка другом с приватностью SOME, видимый тому кто предложил")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_suggest_partner_gift_to_friend_and_accept_privacy_some_1(self):
        """Предложение partner подарка другу, принятие подарка другом с приватностью SOME, видимый тому кто предложил"""
        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        main_page_1 = MainPage(self.driver)

        test_name_this = ""
        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()
        test_ss_name = "test_suggest_partner_gift_to_friend_and_accept_privacy_some_1"

        # Аутентификация и удаление пользователей перед тестом
        with allure.step("Аутентификация и удаление пользователей перед тестом"):
            auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend2)
        auth_controller.authenticate_and_register_user(TestData.phone_friend1, "Firsty", "11", "1111")
        auth_controller.authenticate_and_register_user(TestData.phone_friend2, "Vtoroy", "12", "1111")

        try:
            # Аутентификация
            with allure.step("Аутентификация пользователей"):
                time.sleep(2)
                main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)
                time.sleep(2)

                time.sleep(2)
                main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend2, TestData.confirm_code)
                time.sleep(2)
                main_page_1.register_new_user(self.driver, TestData.phone_friend2)
                time.sleep(2)

            with allure.step("Проверка видимости кнопки настроек профиля"):
                self.assertTrue(
                    main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                    "Кнопка настроек профиля не видна!"
                )
                # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")

            # Обновление контактов
            with allure.step("Обновление контактов на устройстве 1"):
                time.sleep(2)
                main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
                time.sleep(2)
                main_page_1.swipe_down(1999)
                time.sleep(2)

            with allure.step("Обновление контактов на устройстве 2"):
                time.sleep(2)
                main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
                time.sleep(2)
                main_page_1.swipe_down(1999)
                time.sleep(2)

            # Добавление желания на устройстве 1
            with allure.step("Добавление желания на устройстве 1"):
                time.sleep(2)
                main_page_1.click(TestData.BOTTOM_CATALOG_BTN)
                # TelegramReport.send_tg("click(MainPage.CATALOG_BOTTOM_BUTTON_BOUNDS)")
                time.sleep(5)
                main_page_1.click(TestData.catalog_search_field)
                # TelegramReport.send_tg("CATALOG_CATEGORIES_BUTTON clicked on phone 1")
                time.sleep(2)
                main_page_1.send_keys_simple(TestData.partner_wish)
                time.sleep(2)
                main_page_1.click(TestData.catalog_search_field_result)
                time.sleep(5)
                main_page_1.click_by_uiautomator(TestData.CATEGORY_ITEM_1)
                # TelegramReport.send_tg("goods_list_first_good clicked on phone 1")
                time.sleep(2)
                main_page_1.scroll_until_visible(self.driver, MainPage.SUGGEST_GIFT_TO_FRIEND_BUTTON)
                time.sleep(2)
                main_page_1.click(MainPage.SUGGEST_GIFT_TO_FRIEND_BUTTON)
                # TelegramReport.send_tg("SUGGEST_GIFT_TO_FRIEND_BUTTON clicked on phone 1")
                time.sleep(2)
                main_page_1.click_element_by_bounds(TestData.catalog_suggest_wish_first_friend)
                time.sleep(2)
                main_page_1.click(MainPage.SUGGEST_WISH_BUTTON)
                # TelegramReport.send_tg("ADD_TO_WISHES_BUTTON clicked on phone 1")

            with allure.step("Проверка уведомления о предложении подарка"):
                self.assertTrue(
                    main_page_1.is_element_visible(MainPage.NOTIFICATION_WISH_SUGGESTED_TO_FRIEND),
                    "Уведомление о предложении подарка не видно!"
                )
                self.assertTrue(
                    main_page_1.is_element_invisible(MainPage.NOTIFICATION_WISH_SUGGESTED_TO_FRIEND),
                    "Уведомление о предложении подарка не исчезло!"
                )
                # TelegramReport.send_tg("NOTIFICATION_WISH_SUGGESTED visible main_page_1")

            # Скриншот: после добавления желания на устройстве 1
            action_taken = "_after_wish_add_phone1"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)

            with allure.step("Снимок экрана с эталонным изображением после добавления желания (устройство 1)"):
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
                allure.attach.file(ss_etalon, name="Эталонный скриншот", attachment_type=allure.attachment_type.PNG)

            with allure.step("Снимок экрана с результатом выполнения теста (устройство 1)"):
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
                allure.attach.file(ss_run, name="Скриншот результата", attachment_type=allure.attachment_type.PNG)

            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), "Сравнение изображений не удалось"

            # Принятие желания на устройстве 2
            with allure.step("Принятие желания на устройстве 2"):
                main_page_1.click(TestData.BOTTOM_WISHES_BTN)
                # TelegramReport.send_tg("click(TestData.BOTTOM_WISHES_BTN) called")
                time.sleep(3)
                main_page_1.swipe_up(600)
                time.sleep(2)
                main_page_1.click(MainPage.ACCEPT_WISH_BUTTON)
                # TelegramReport.send_tg("click(MainPage.ACCEPT_WISH_BUTTON) called")

            with allure.step("Настройка принятого желания"):
                time.sleep(2)
                main_page_1.click(MainPage.ADD_WISH_WITH_SETTINGS)
                # TelegramReport.send_tg("click(MainPage.ADD_WISH_WITH_SETTINGS) called")
                time.sleep(2)
                main_page_1.click_element_by_bounds(TestData.accept_suggested_wish_desc_field)
                # TelegramReport.send_tg("click(MainPage.DESCRIPTION_FILED) called")
                time.sleep(2)
                main_page_1.send_keys_simple("test gift desc")
                # TelegramReport.send_tg("send_keys(MainPage.DESCRIPTION_FILED, 'test gift desc') called")
                time.sleep(2)
                main_page_1.scroll_down(self.driver, 1)
                # TelegramReport.send_tg("scroll_down 1")
                time.sleep(2)
                main_page_1.click_element_by_bounds(TestData.suggested_partner_wish_privacy_some)
                # TelegramReport.send_tg("click(MainPage.PRIVACY_SOME_BOUNDS) called")
                time.sleep(2)
                main_page_1.click_by_uiautomator_desc_contains(TestData.choose_friends_first)
                time.sleep(2)
                main_page_1.click_element_by_bounds(MainPage.FINAL_ACCEPT_BONDS)
                # TelegramReport.send_tg("click(MainPage.FINAL_ACCEPT_BONDS) called")

            with allure.step("Проверка уведомления о добавлении желания"):
                self.assertTrue(
                    main_page_1.is_element_visible(MainPage.NOTIFICATION_WISH_ADDED),
                    "Уведомление о добавлении желания не видно!"
                )
                # TelegramReport.send_tg("NOTIFICATION_WISH_SUGGESTED visible main_page_1")
                self.assertTrue(
                    main_page_1.is_element_invisible(MainPage.NOTIFICATION_WISH_ADDED),
                    "Уведомление о добавлении желания не исчезло!"
                )

            # Скриншот: после принятия желания на устройстве 2
            action_taken = "_after_wish_accept_phone2"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)

            with allure.step("Снимок экрана с эталонным изображением после принятия желания (устройство 2)"):
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
                allure.attach.file(ss_etalon, name="Эталонный скриншот", attachment_type=allure.attachment_type.PNG)

            with allure.step("Снимок экрана с результатом выполнения теста (устройство 2)"):
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
                allure.attach.file(ss_run, name="Скриншот результата", attachment_type=allure.attachment_type.PNG)

            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), "Сравнение изображений не удалось"

            # Проверка видимости подарка на устройстве 1
            with allure.step("Проверка видимости подарка на устройстве 1"):
                main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
                time.sleep(2)
                main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
                # TelegramReport.send_tg("click(TestData.first_friend_bonds)")
                time.sleep(4)

            # Скриншот: проверка видимости подарка на устройстве 1
            action_taken = "_after_wish_accept_visible_phone1"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)

            with allure.step("Снимок экрана с эталонным изображением видимости подарка (устройство 1)"):
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
                allure.attach.file(ss_etalon, name="Эталонный скриншот", attachment_type=allure.attachment_type.PNG)

            with allure.step("Снимок экрана с результатом выполнения теста (видимость подарка, устройство 1)"):
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
                allure.attach.file(ss_run, name="Скриншот результата", attachment_type=allure.attachment_type.PNG)

            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), "Сравнение изображений не удалось"

            # Разлогин и вход третьим пользователем
            with allure.step("Разлогин и вход третьим пользователем"):
                time.sleep(2)
                main_page_1.logout(self.driver)
                time.sleep(2)
                main_page_1.auth_by_phone(TestData.phone_friend3, TestData.confirm_code)
                time.sleep(2)
                main_page_1.register_new_user(self.driver, TestData.phone_friend2)
                time.sleep(2)

            # Проверка видимости подарка третьим пользователем
            with allure.step("Проверка видимости подарка третьим пользователем"):
                main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
                time.sleep(2)
                main_page_1.swipe_down(999)
                time.sleep(4)
                main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
                time.sleep(4)

            # Скриншот: проверка видимости подарка третьим пользователем
            action_taken = "_wish_not_visible_under_phone3"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)

            with allure.step("Снимок экрана с эталонным изображением (подарок не виден третьему пользователю)"):
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
                allure.attach.file(ss_etalon, name="Эталонный скриншот", attachment_type=allure.attachment_type.PNG)

            with allure.step("Снимок экрана с результатом выполнения теста (подарок не виден третьему пользователю)"):
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
                allure.attach.file(ss_run, name="Скриншот результата", attachment_type=allure.attachment_type.PNG)

            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), "Сравнение изображений не удалось"

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

    @pytest.mark.suggest_wish_tests
    @allure.story(
        "Test Case: Предложение partner желания из каталога и принятие его другом с видимостью для нескольких юзеров но не друга предложившего желание")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_suggest_partner_gift_to_friend_and_accept_privacy_some_2(self):
        """Предложение partner желания из каталога и принятие его другом с видимостью для нескольких юзеров но не друга предложившего желание"""
        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        main_page_1 = MainPage(self.driver)

        test_name_this = ""
        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()
        test_ss_name = "test_suggest_partner_gift_to_friend_and_accept_privacy_some_2"

        # Authenticate and delete users before the test
        with allure.step("Аутентификация и удаление пользователей перед тестом"):
            auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend2)
        auth_controller.authenticate_and_register_user(TestData.phone_friend1, "Firsty", "11", "1111")
        auth_controller.authenticate_and_register_user(TestData.phone_friend2, "Vtoroy", "12", "1111")

        try:
            # Auth
            with allure.step("Аутентификация пользователей"):
                time.sleep(2)
                main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)
                time.sleep(2)

                time.sleep(2)
                main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend2, TestData.confirm_code)
                time.sleep(2)
                main_page_1.register_new_user(self.driver, TestData.phone_friend2)
                time.sleep(2)

            with allure.step("Проверка видимости кнопки настроек профиля"):
                self.assertTrue(
                    main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                    "Profile settings button not visible!"
                )
                # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")

            # refresh contacts
            with allure.step("Обновление контактов на первом устройстве"):
                time.sleep(2)
                main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
                time.sleep(2)
                main_page_1.swipe_down(1999)
                time.sleep(2)

            with allure.step("Обновление контактов на втором устройстве"):
                time.sleep(2)
                main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
                time.sleep(2)
                main_page_1.swipe_down(1999)
                time.sleep(2)

            # Start phone 1
            # add wish
            with allure.step("Добавление желания на первом устройстве"):
                time.sleep(2)
                main_page_1.click(TestData.BOTTOM_CATALOG_BTN)
                # TelegramReport.send_tg("click(MainPage.CATALOG_BOTTOM_BUTTON_BOUNDS)")
                time.sleep(5)
                main_page_1.click(TestData.catalog_search_field)
                # TelegramReport.send_tg("CATALOG_CATEGORIES_BUTTON clicked on phone 1")
                time.sleep(2)
                main_page_1.send_keys_simple(TestData.partner_wish)
                time.sleep(2)
                main_page_1.click(TestData.catalog_search_field_result)
                time.sleep(5)
                main_page_1.click_by_uiautomator(TestData.CATEGORY_ITEM_1)
                # TelegramReport.send_tg("goods_list_first_good clicked on phone 1")
                time.sleep(2)
                main_page_1.scroll_until_visible(self.driver, MainPage.SUGGEST_GIFT_TO_FRIEND_BUTTON)
                time.sleep(2)
                main_page_1.click(MainPage.SUGGEST_GIFT_TO_FRIEND_BUTTON)
                # TelegramReport.send_tg("SUGGEST_GIFT_TO_FRIEND_BUTTON clicked on phone 1")
                time.sleep(2)
                main_page_1.click_element_by_bounds(TestData.catalog_suggest_wish_first_friend)
                time.sleep(2)
                main_page_1.click(MainPage.SUGGEST_WISH_BUTTON)
                # TelegramReport.send_tg("ADD_TO_WISHES_BUTTON clicked on phone 1")

            with allure.step("Проверка отображения уведомления о предложении желания"):
                self.assertTrue(
                    main_page_1.is_element_visible(MainPage.NOTIFICATION_WISH_SUGGESTED_TO_FRIEND),
                    "NOTIFICATION_WISH_SUGGESTED not visible!"
                )
                self.assertTrue(
                    main_page_1.is_element_invisible(MainPage.NOTIFICATION_WISH_SUGGESTED_TO_FRIEND),
                    "NOTIFICATION_WISH_SUGGESTED not visible!"
                )
                # TelegramReport.send_tg("NOTIFICATION_WISH_SUGGESTED visible main_page_1")

            # Screenshot block
            with allure.step("Снимок экрана после добавления желания на первом устройстве"):
                action_taken = "_after_wish_add_phone1"
                ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
                ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
                allure.attach.file(ss_etalon, name="Etalon Screenshot", attachment_type=allure.attachment_type.PNG)
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
                allure.attach.file(ss_run, name="Run Screenshot", attachment_type=allure.attachment_type.PNG)
                time.sleep(1)
                assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Start phone 2 accept privacy only me
            with allure.step("Принятие желания на втором устройстве с настройками приватности"):
                main_page_1.click(TestData.BOTTOM_WISHES_BTN)
                # TelegramReport.send_tg("click(TestData.BOTTOM_WISHES_BTN) called")
                time.sleep(3)
                main_page_1.swipe_up(600)
                time.sleep(2)
                main_page_1.click(MainPage.ACCEPT_WISH_BUTTON)
                # TelegramReport.send_tg("click(MainPage.ACCEPT_WISH_BUTTON) called")
                time.sleep(2)

                main_page_1.click(MainPage.ADD_WISH_WITH_SETTINGS)
                # TelegramReport.send_tg("click(MainPage.ADD_WISH_WITH_SETTINGS) called")
                time.sleep(2)
                main_page_1.click_element_by_bounds(TestData.accept_suggested_wish_desc_field)
                # TelegramReport.send_tg("click(MainPage.DESCRIPTION_FILED) called")
                time.sleep(2)
                main_page_1.send_keys_simple("test gift desc")
                # TelegramReport.send_tg("send_keys(MainPage.DESCRIPTION_FILED, 'test gift desc') called")
                time.sleep(2)

                main_page_1.scroll_down(self.driver, 1)
                # TelegramReport.send_tg("scroll_down 1")
                time.sleep(2)
                main_page_1.click_element_by_bounds(TestData.suggested_partner_wish_privacy_some)
                # TelegramReport.send_tg("click(MainPage.PRIVACY_ONLY_ME_BOUNDS) called")
                time.sleep(2)
                # выбираем second друга
                main_page_1.click_element_by_bounds(TestData.choose_friends_second)
                time.sleep(2)
                main_page_1.click_element_by_bounds(MainPage.FINAL_ACCEPT_BONDS)
                # TelegramReport.send_tg("click(MainPage.FINAL_ACCEPT_BONDS) called")

            with allure.step("Проверка отображения уведомления о добавлении желания"):
                self.assertTrue(
                    main_page_1.is_element_visible(MainPage.NOTIFICATION_WISH_ADDED),
                    "NOTIFICATION_WISH_SUGGESTED not visible!"
                )
                # TelegramReport.send_tg("NOTIFICATION_WISH_SUGGESTED visible main_page_1")
                self.assertTrue(
                    main_page_1.is_element_invisible(MainPage.NOTIFICATION_WISH_ADDED),
                    "NOTIFICATION_WISH_SUGGESTED visible!"
                )

            # Screenshot block
            with allure.step("Снимок экрана после принятия желания на втором устройстве"):
                action_taken = "_after_wish_accept_phone2"
                ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
                ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
                allure.attach.file(ss_etalon, name="Etalon Screenshot", attachment_type=allure.attachment_type.PNG)
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
                allure.attach.file(ss_run, name="Run Screenshot", attachment_type=allure.attachment_type.PNG)
                time.sleep(1)
                assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # проверка видимости под первым
            with allure.step("Проверка видимости желания под первым пользователем"):
                main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
                time.sleep(2)
                main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
                # TelegramReport.send_tg("click(TestData.first_friend_bonds)")
                time.sleep(4)

            # Screenshot block
            with allure.step("Снимок экрана после проверки видимости желания на первом устройстве"):
                action_taken = "_after_wish_accept_visible_phone1"
                ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
                ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
                allure.attach.file(ss_etalon, name="Etalon Screenshot", attachment_type=allure.attachment_type.PNG)
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
                allure.attach.file(ss_run, name="Run Screenshot", attachment_type=allure.attachment_type.PNG)
                time.sleep(1)
                assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Разлогин
            with allure.step("Разлогин второго пользователя"):
                time.sleep(2)
                main_page_1.logout(self.driver)
                time.sleep(2)

            # Логин третьим
            with allure.step("Аутентификация третьего пользователя"):
                main_page_1.auth_by_phone(TestData.phone_friend3, TestData.confirm_code)
                time.sleep(2)
                main_page_1.register_new_user(self.driver, TestData.phone_friend2)
                time.sleep(2)

            # Проверка под третьим юзером
            with allure.step("Проверка видимости желания под третьим пользователем"):
                main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
                time.sleep(2)
                main_page_1.swipe_down(999)
                time.sleep(4)
                main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
                time.sleep(4)

            # Screenshot block
            with allure.step("Снимок экрана после проверки видимости желания на третьем устройстве"):
                action_taken = "_wish_not_visible_under_phone3"
                ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
                ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
                allure.attach.file(ss_etalon, name="Etalon Screenshot", attachment_type=allure.attachment_type.PNG)
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
                allure.attach.file(ss_run, name="Run Screenshot", attachment_type=allure.attachment_type.PNG)
                time.sleep(1)
                assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

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
