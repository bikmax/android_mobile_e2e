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


class CustomWish(BaseTest):
    @pytest.mark.regress
    @pytest.mark.custom_wish_tests
    def test_suggest_custom_gift_and_accept_visible_all(self):
        """BUG: /-/issues/2975  """
        main_page_1 = MainPage(self.driver)

        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        #status = "🔴"
        status = "🟡"
        bug_link = "/-/issues/2975"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = "Сторонние Желания: Предложение стороннего желания(ссылкой), его принятие(через мои желания) и исполнение"
        test_ss_name = "test_suggest_custom_gift_and_accept_visible_all"


        # Authenticate and delete users before the test
        auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend2)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend3)
        auth_controller.authenticate_and_register_user(TestData.phone_friend1, "Firsty", "11", "1111")
        auth_controller.authenticate_and_register_user(TestData.phone_friend2, "Vtoroy", "12", "1111")
        auth_controller.authenticate_and_register_user(TestData.phone_friend3, "Treti", "12", "1111")

        try:
            # Auth user 1
            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)
            time.sleep(6)


            with allure.step("Выбор друга для отправки кастомного желания"):
                # refresh contacts
                time.sleep(2)
                main_page_1.is_element_visible(TestData.BOTTOM_FRIENDS_BTN_XP)
                main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
                main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
                #TelegramReport.send_tg("click(.custom_wish_add_button)")
                time.sleep(2)
                main_page_1.click(MainPage.SUGGEST_WISH_TO_FRIEND)
                #TelegramReport.send_tg("click(.custom_wish_add_button)")
                time.sleep(2)
                main_page_1.click(MainPage.SUGGEST_WISH_BUTTON)
                #TelegramReport.send_tg("click(.custom_wish_add_button)")
                time.sleep(2)

            with allure.step("Добавление кастомного желания с ссылкой"):
                main_page_1.click(MainPage.ADD_CUSTOM_WISH_LINK)
                #TelegramReport.send_tg("click(MainPage.ADD_CUSTOM_WISH_LINK)")
                time.sleep(2)

                main_page_1.send_keys(MainPage.ADD_CUSTOM_WISH_LINK, TestData.parseWildberries)
                #TelegramReport.send_tg("send_keys(TestData.parseWildberries)")
                time.sleep(2)
                self.driver.hide_keyboard()

            with allure.step("Завершение добавления кастомного желания"):
                time.sleep(2)
                main_page_1.click(TestData.next_button)
                #TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")
                time.sleep(35)
                main_page_1.click(TestData.next_button)
                time.sleep(5)
                main_page_1.click(MainPage.DONE_BUTTON)


            # Принятие через мои желания
            with allure.step("Relogin на устройстве 2"):
                main_page_1.logout(self.driver)
                time.sleep(5)
                main_page_1.auth_by_phone(TestData.phone_friend3, TestData.confirm_code)
                time.sleep(5)
                main_page_1.is_element_visible(TestData.BOTTOM_WISHES_BTN)
                main_page_1.click(TestData.BOTTOM_WISHES_BTN)
                time.sleep(8)
                main_page_1.is_element_visible(MainPage.ACCEPT_WISH_BUTTON)
                main_page_1.click(MainPage.ACCEPT_WISH_BUTTON)
                time.sleep(5)
                main_page_1.is_element_visible(MainPage.ADD_WISH_WITHOUT_SETTINGS)
                main_page_1.click(MainPage.ADD_WISH_WITHOUT_SETTINGS)
                time.sleep(5)

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
    @pytest.mark.custom_wish_tests
    def test_add_custom_gift_visible_only_me(self):
        main_page_1 = MainPage(self.driver)

        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = "Создание кастомного желания с доступностью только себе"
        test_ss_name = "test_reserve_custom_friend_gift"

        # Authenticate and delete users before the test
        with allure.step("Аутентификация и удаление пользователей перед тестом"):
            auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
            auth_controller.authenticate_and_delete_user(TestData.phone_friend2)
            auth_controller.authenticate_and_delete_user(TestData.phone_friend3)
            auth_controller.authenticate_and_register_user(TestData.phone_friend1, "Firsty", "11", "1111")
            auth_controller.authenticate_and_register_user(TestData.phone_friend2, "Vtoroy", "12", "1111")
            auth_controller.authenticate_and_register_user(TestData.phone_friend3, "Treti", "12", "1111")

        try:
            # Auth user 1
            with allure.step("Аутентификация первого пользователя"):
                main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)
            # Navigate to add custom gift
            with allure.step("Переход к добавлению пользовательского подарка"):
                main_page_1.add_custom_wish(TestData.parseWildberries)

                main_page_1.is_element_visible(TestData.PRIVACY_BUTTON_ONLYME)
                main_page_1.click_by_uiautomator(TestData.PRIVACY_BUTTON_ONLYME)
                main_page_1.is_element_visible(TestData.PRIVACY_BUTTON_ONLYME)
                main_page_1.click(MainPage.DONE_BUTTON)


            # Проверяем вторым пользователем что подарок видно
            with allure.step("Проверка видимости подарка вторым пользователем"):
                main_page_1.logout(self.driver)
                main_page_1.auth_by_phone(TestData.phone_friend3, TestData.confirm_code)
                main_page_1.is_element_visible(TestData.BOTTOM_FRIENDS_BTN_XP)
                main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
                main_page_1.is_element_visible(TestData.CONTACTS_FRIEND_1)
                main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
                main_page_1.is_element_visible(TestData.friend_have_no_wishes)
                main_page_1.is_element_invisible(TestData.friend_wish_first_wish)

                time.sleep(4)


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
    @pytest.mark.custom_wish_tests
    def test_add_custom_gift_visible_some(self):
        """Создание кастомного желания с доступностью для нескольких пользователей"""
        main_page_1 = MainPage(self.driver)

        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = "Создание кастомного желания с доступностью для нескольких пользователей"
        test_ss_name = "test_add_custom_gift_visible_some"

        # Authenticate and delete users before the test
        auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend2)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend3)
        auth_controller.authenticate_and_register_user(TestData.phone_friend1, "Firsty", "11", "1111")
        auth_controller.authenticate_and_register_user(TestData.phone_friend2, "Vtoroy", "12", "1111")
        auth_controller.authenticate_and_register_user(TestData.phone_friend3, "Treti", "13", "1111")

        try:
            # Auth user 1
            with allure.step("Аутентификация первого пользователя"):
                main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)

            # with allure.step("Проверка видимости кнопки настроек профиля"):
            #     self.assertTrue(main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
            #                     "Profile settings button not visible!")

            # Navigate to add custom gift
            with allure.step("Переход к добавлению пользовательского подарка"):
                main_page_1.click(TestData.BOTTOM_WISHES_BTN)
                time.sleep(2)

                main_page_1.click(MainPage.ADD_WISH_BUTTON)
                # TelegramReport.send_tg("click(MainPage.ADD_WISH_BUTTON)")
                time.sleep(2)

                main_page_1.click(TestData.custom_wish_add_button)
                # TelegramReport.send_tg("click(.custom_wish_add_button)")
                time.sleep(2)

                main_page_1.click(MainPage.ADD_CUSTOM_WISH_LINK)
                # TelegramReport.send_tg("click(MainPage.ADD_CUSTOM_WISH_LINK)")
                time.sleep(2)

                main_page_1.send_keys(MainPage.ADD_CUSTOM_WISH_LINK, TestData.parseWildberries)
                # TelegramReport.send_tg("send_keys(TestData.parseWildberries)")
                time.sleep(2)

            # Finalize custom gift addition
            with allure.step("Завершение добавления пользовательского подарка"):
                main_page_1.click(TestData.next_button)
                # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")
                time.sleep(40)
                main_page_1.click(TestData.next_button)
                # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")
                time.sleep(4)

                main_page_1.click(TestData.next_button)
                time.sleep(2)
                main_page_1.click_by_uiautomator(TestData.PRIVACY_BUTTON_SOME)
                main_page_1.click(TestData.next_button)
                time.sleep(5)
                main_page_1.click(TestData.PRIVACY_SOME_SELECT_FRIEND_1)
                time.sleep(2)
                main_page_1.click(MainPage.DONE_BUTTON)
                main_page_1.is_element_visible(TestData.MY_WISHES_FIRST_WISH)
                time.sleep(5)

            # Проверяем 2 пользователем что подарок  видно
            with allure.step("Проверка видимости подарка вторым пользователем"):
                main_page_1.logout(self.driver)
                time.sleep(2)
                main_page_1.auth_by_phone(TestData.phone_friend2, TestData.confirm_code)
                time.sleep(2)
                main_page_1.is_element_visible(TestData.BOTTOM_FRIENDS_BTN_XP)
                main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
                time.sleep(2)
                main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
                time.sleep(4)
                main_page_1.is_element_visible(TestData.friend_wish_first_wish)


            # Проверяем 3 пользователем что подарок NE видно
            with allure.step("Проверка видимости подарка вторым пользователем"):
                main_page_1.logout(self.driver)
                time.sleep(2)
                main_page_1.auth_by_phone(TestData.phone_friend3, TestData.confirm_code)
                time.sleep(2)
                main_page_1.is_element_visible(TestData.BOTTOM_FRIENDS_BTN_XP)
                main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
                time.sleep(2)
                main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
                time.sleep(4)

                main_page_1.is_element_visible(TestData.friend_have_no_wishes)
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

    @pytest.mark.custom_wish_tests
    @pytest.mark.regress
    def test_add_custom_gift_negative(self):
        """Создание кастомного желания NEGATIVE"""
        main_page_1 = MainPage(self.driver)

        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = "Создание кастомного желания NEGATIVE"
        test_ss_name = "test_add_custom_gift_negative"

        # Authenticate and delete users before the test
        auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        auth_controller.authenticate_and_register_user(TestData.phone_friend1, TestData.friend1_name, "11", "1111")

        try:
            # Auth user 1
            with allure.step("Авторизация пользователя 1"):
                main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)
                


            # Navigate to add custom gift
            with allure.step("Переход к добавлению кастомного подарка"):
                main_page_1.click(MainPage.GIFT_LIST_LOCATOR)
                #TelegramReport.send_tg("click(MainPage.GIFT_LIST_LOCATOR)")
                time.sleep(2)

                main_page_1.click(MainPage.ADD_WISH_BUTTON)
                #TelegramReport.send_tg("click(MainPage.ADD_WISH_BUTTON)")
                time.sleep(2)

                main_page_1.click(TestData.custom_wish_add_button)
                #TelegramReport.send_tg("click(.custom_wish_add_button)")
                time.sleep(2)

            # WRONG URL
            with allure.step("Ввод некорректного URL"):
                main_page_1.click(MainPage.ADD_CUSTOM_WISH_LINK)
                #TelegramReport.send_tg("click(MainPage.ADD_CUSTOM_WISH_LINK)")
                time.sleep(2)

                main_page_1.send_keys_simple("htp:/www.example..com")
                time.sleep(4)
                main_page_1.is_element_visible(TestData.WRONG_LINK_ALERT)

                main_page_1.click(TestData.CLEAR_TF)

                time.sleep(1)
                main_page_1.click(MainPage.NEXT_BUTTON)

                main_page_1.is_element_visible(TestData.CUSTOM_WISH_PRICE_FIELD)
                main_page_1.click(TestData.CUSTOM_WISH_PRICE_FIELD)

                main_page_1.is_element_visible(TestData.CUSTOM_WISH_DESC_FIELD)
                main_page_1.click(TestData.CUSTOM_WISH_DESC_FIELD)

                main_page_1.is_element_visible(TestData.CUSTOM_WISH_PRICE_ALERT)

                main_page_1.is_element_visible(TestData.CUSTOM_WISH_PRICE_FIELD)
                main_page_1.click(TestData.CUSTOM_WISH_PRICE_FIELD)

                main_page_1.send_keys_simple("3333")

                main_page_1.is_element_invisible(TestData.CUSTOM_WISH_PRICE_ALERT)

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
