import logging
import re
import time
import traceback

import pytest

from ResultCollector import ResultCollector
from core.pages.main_page import MainPage
from core.data.test_data import TestData
from reporting.TelegramReport import TelegramReport
from core.pages.base_test import BaseTest
from core.api.AuthController import AuthController


class CustomWish(BaseTest):

    # WILDBERRIES
    @pytest.mark.side_wish_tests
    def test_add_custom_gift_visible_all_wildberries(self):
        """Создание желания с ссылкой на товар из маркетплейса WILDBERRIES с областью видимости Доступно всем"""
        main_page_1 = MainPage(self.driver)

        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = ""
        test_ss_name = "custom_wish_from_wildberries_privacy_all"

        # Authenticate and delete users before the test
        auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend2)
        auth_controller.authenticate_and_register_user(TestData.phone_friend1, "Firsty", "11", "1111")
        auth_controller.authenticate_and_register_user(TestData.phone_friend2, "Vtoroy", "12", "1111")

        try:
            # Auth user 1
            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)
            time.sleep(2)

            time.sleep(2)

            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend2, TestData.confirm_code)
            time.sleep(2)
            main_page_1.register_new_user(self.driver, TestData.phone_friend2)
            time.sleep(2)

            self.assertTrue(main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                            "Profile settings button not visible!")
            # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")
            self.assertTrue(main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                            "Profile settings button not visible!")
            # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")

            # Navigate to add custom gift
            main_page_1.click(MainPage.GIFT_LIST_LOCATOR)
            # TelegramReport.send_tg("click(MainPage.GIFT_LIST_LOCATOR)")
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
            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")

            time.sleep(40)

            # Screenshot block
            action_taken = "_custom_wish_added_parsed_text_fields"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")
            time.sleep(4)

            # Screenshot block
            action_taken = "_custom_wish_added_parsed_photos"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")
            time.sleep(2)

            main_page_1.click(MainPage.DONE_BUTTON)
            # TelegramReport.send_tg("click(MainPage.DONE_BUTTON)")

            main_page_1.click(TestData.BOTTOM_WISHES_BTN)
            # TelegramReport.send_tg("click(MainPage.WISHMY)")
            time.sleep(3)

            # Screenshot block
            action_taken = "_custom_wish_after_adding_check_wish_is_displayed"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(2)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Проверяем вторым пользователем что подарок видно
            main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
            time.sleep(2)
            main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
            time.sleep(4)

            # Screenshot block
            action_taken = "_privacy_all_check_by_second_phone"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(2)
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

    @pytest.mark.side_wish_tests
    def test_add_custom_gift_visible_only_me_wildberries(self):
        """Создание желания с ссылкой на товар из маркетплейса WILDBERRIES с областью видимости Доступно Только мне"""
        main_page_1 = MainPage(self.driver)

        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = ""
        test_ss_name = "custom_wish_from_wildberries_privacy_only_me"

        # Authenticate and delete users before the test
        auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend2)
        auth_controller.authenticate_and_register_user(TestData.phone_friend1, "Firsty", "11", "1111")
        auth_controller.authenticate_and_register_user(TestData.phone_friend2, "Vtoroy", "12", "1111")

        try:
            # Auth user 1
            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)

            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend2, TestData.confirm_code)
            main_page_1.register_new_user(self.driver, TestData.phone_friend2)
            main_page_1.logout(self.driver)
            main_page_1.auth_by_phone(TestData.phone_friend2, TestData.confirm_code)

            self.assertTrue(main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                            "Profile settings button not visible!")
            # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")
            self.assertTrue(main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                            "Profile settings button not visible!")
            # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")

            # Navigate to add custom gift
            main_page_1.click(MainPage.GIFT_LIST_LOCATOR)
            # TelegramReport.send_tg("click(MainPage.GIFT_LIST_LOCATOR)")
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

            # Добавили ссылку, жмем далее
            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")

            time.sleep(40)

            # Screenshot block
            action_taken = "_custom_wish_added_parsed_text_fields"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Дождались загрузки результата парсера, жмем далее
            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")
            time.sleep(4)

            # Screenshot block
            action_taken = "_custom_wish_added_parsed_photos"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Дождались загрузки фоток с парсера, жмем далее
            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")
            time.sleep(2)

            # Выбираем приватность
            main_page_1.click_by_uiautomator_desc_contains(MainPage.PRIVACY_ONLY_ME_DESC)
            # TelegramReport.send_tg("click(MainPage.PRIVACY_ONLY_ME_BOUNDS)")

            # Выбрали приватность, жмем Готово
            main_page_1.click(MainPage.DONE_BUTTON)
            time.sleep(3)

            main_page_1.click(TestData.BOTTOM_WISHES_BTN)
            # TelegramReport.send_tg("click(MainPage.WISHMY)")
            time.sleep(3)

            # Screenshot block
            action_taken = "_custom_wish_after_adding_check_wish_is_displayed"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(2)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Проверяем вторым пользователем что подарок видно
            main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
            time.sleep(2)
            main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
            time.sleep(4)
            main_page_1.swipe_up(600)

            # Screenshot block
            action_taken = "_privacy_all_check_by_second_phone"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(2)
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

    @pytest.mark.side_wish_tests
    def test_add_custom_gift_visible_some_wildberries(self):
        """Создание желания с ссылкой на товар из маркетплейса WILDBERRIES с областью видимости Доступно Некоторым"""
        main_page_1 = MainPage(self.driver)

        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = ""
        test_ss_name = "test_add_custom_gift_visible_some_wildberries"

        # Authenticate and delete users before the test
        auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend2)
        auth_controller.authenticate_and_register_user(TestData.phone_friend1, "Firsty", "11", "1111")
        auth_controller.authenticate_and_register_user(TestData.phone_friend2, "Vtoroy", "12", "1111")
        auth_controller.authenticate_and_delete_user(TestData.phone_friend3)

        try:
            # Auth user 1
            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)

            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend2, TestData.confirm_code)
            main_page_1.register_new_user(self.driver, TestData.phone_friend2)
            main_page_1.logout(self.driver)
            main_page_1.auth_by_phone(TestData.phone_friend2, TestData.confirm_code)

            self.assertTrue(main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                            "Profile settings button not visible!")
            # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")
            self.assertTrue(main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                            "Profile settings button not visible!")
            # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")

            # Navigate to add custom gift
            main_page_1.click(MainPage.GIFT_LIST_LOCATOR)
            # TelegramReport.send_tg("click(MainPage.GIFT_LIST_LOCATOR)")
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

            # Добавили ссылку, жмем далее
            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")

            time.sleep(40)

            # Screenshot block
            action_taken = "_custom_wish_added_parsed_text_fields"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Дождались загрузки результата парсера, жмем далее
            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")
            time.sleep(4)

            # Screenshot block
            action_taken = "_custom_wish_added_parsed_photos"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Дождались загрузки фоток с парсера, жмем далее
            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")
            time.sleep(2)

            # Выбираем приватность
            main_page_1.click_by_uiautomator_desc_contains(MainPage.PRIVACY_SOME_DESC)
            time.sleep(2)
            # TelegramReport.send_tg("click(MainPage.PRIVACY_SOME)")

            # Выбрали приватность, жмем Готово
            main_page_1.click(MainPage.DONE_BUTTON)
            time.sleep(3)

            # Выбираем друга TODO ждем бага пока починят выбор
            main_page_1.click_by_uiautomator_desc_contains(TestData.choose_friends_first)
            time.sleep(1)

            # Выбрали друга, жмем Готово
            main_page_1.click(MainPage.DONE_BUTTON)
            # TelegramReport.send_tg("click(MainPage.DONE_BUTTON)")

            # Проверяем что подарок добавлен
            main_page_1.click(TestData.BOTTOM_WISHES_BTN)
            # TelegramReport.send_tg("click(MainPage.WISHMY)")
            time.sleep(3)

            # Screenshot block
            action_taken = "_custom_wish_after_adding_check_wish_is_displayed"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(2)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Проверяем вторым пользователем что подарок видно
            main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
            time.sleep(2)
            main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
            time.sleep(4)
            main_page_1.swipe_up(600)

            # Screenshot block
            action_taken = "_privacy_some_check_by_second_phone"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(2)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Проверяем третьим пользователем что подарок НЕ видно
            main_page_1.logout(self.driver)
            main_page_1.auth_by_phone(TestData.phone_friend3, TestData.confirm_code)
            main_page_1.register_new_user(self.driver, TestData.phone_friend2)
            time.sleep(2)
            main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
            time.sleep(2)
            main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
            time.sleep(4)
            main_page_1.swipe_up(600)

            # Screenshot block
            action_taken = "_privacy_some_check_by_third_phone"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(2)
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

    @pytest.mark.side_wish_tests
    def test_add_custom_gift_with_edit_and_visible_some_wildberries(self):
        """Создание желания с ссылкой на товар из маркетплейса WILDBERRIES, редактированием спарсенных полей и с областью видимости Доступно Некоторым"""
        main_page_1 = MainPage(self.driver)

        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = ""
        test_ss_name = "test_add_custom_gift_with_edit_and_visible_some_wildberries"

        # Authenticate and delete users before the test
        auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend2)
        auth_controller.authenticate_and_register_user(TestData.phone_friend1, "Firsty", "11", "1111")
        auth_controller.authenticate_and_register_user(TestData.phone_friend2, "Vtoroy", "12", "1111")
        auth_controller.authenticate_and_delete_user(TestData.phone_friend3)

        try:
            # Auth user 1
            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)

            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend2, TestData.confirm_code)
            main_page_1.register_new_user(self.driver, TestData.phone_friend2)
            main_page_1.logout(self.driver)
            main_page_1.auth_by_phone(TestData.phone_friend2, TestData.confirm_code)

            self.assertTrue(main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                            "Profile settings button not visible!")
            # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")
            self.assertTrue(main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                            "Profile settings button not visible!")
            # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")

            # Navigate to add custom gift
            main_page_1.click(MainPage.GIFT_LIST_LOCATOR)
            # TelegramReport.send_tg("click(MainPage.GIFT_LIST_LOCATOR)")
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

            # Добавили ссылку, жмем далее
            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")

            time.sleep(40)

            # Дождались парсера, редактируем данные
            # Поле Имя
            main_page_1.click_element_by_bounds(TestData.custom_wish_name_field)
            time.sleep(1)
            main_page_1.clear_text_field_simple(self.driver)
            time.sleep(1)
            main_page_1.send_keys_simple("Test Name Of Wish Customized")
            time.sleep(1)
            # Поле Стоимость
            main_page_1.click_element_by_bounds(TestData.custom_wish_price_field)
            time.sleep(1)
            main_page_1.clear_text_field_simple(self.driver)
            time.sleep(1)
            main_page_1.send_keys_simple("5555")
            time.sleep(1)
            # Поле Описание
            main_page_1.click_element_by_bounds(TestData.custom_wish_description_field)
            time.sleep(1)
            main_page_1.clear_text_field_simple(self.driver)
            time.sleep(1)
            main_page_1.send_keys_simple("custom wish description not so long")
            time.sleep(1)

            # Screenshot того как было заполнено желание
            action_taken = "_custom_wish_edited_parsed_text_fields"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Дождались загрузки результата парсера, жмем далее
            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")
            time.sleep(4)

            # Screenshot block
            action_taken = "_custom_wish_added_parsed_photos"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Дождались загрузки фоток с парсера, жмем далее
            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")
            time.sleep(2)

            # Выбираем приватность
            # main_page_1.click_by_uiautomator_desc_contains(MainPage.PRIVACY_SOME_DESC) TODO
            # main_page_1.click_element_by_bounds(MainPage.PRIVACY_ALL)
            time.sleep(2)
            # TelegramReport.send_tg("click(MainPage.PRIVACY_SOME)")

            # Выбрали приватность, жмем Готово
            main_page_1.click(MainPage.DONE_BUTTON)
            time.sleep(3)

            # Выбираем друга TODO ждем бага пока починят выбор
            # main_page_1.click_by_uiautomator_desc_contains(TestData.choose_friends_first)
            time.sleep(1)

            # Выбрали друга, жмем Готово
            # main_page_1.click(MainPage.DONE_BUTTON) TODO
            # TelegramReport.send_tg("click(MainPage.DONE_BUTTON)")

            # Проверяем что подарок добавлен и видно кастомные поля
            main_page_1.click(TestData.BOTTOM_WISHES_BTN)
            # TelegramReport.send_tg("click(MainPage.WISHMY)")
            time.sleep(3)
            main_page_1.click_by_uiautomator(TestData.MY_WISHES_FIRST_WISH)
            time.sleep(3)
            # Screenshot после открытия подарка
            action_taken = "_custom_wish_after_adding_check_wish_is_displayed"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(2)
            # Compare screenshots and assert result
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Скроллим вниз чтобы увидеть описание товара
            main_page_1.swipe_up(1300)
            time.sleep(2)

            # Screenshot block
            action_taken = "_custom_wish_after_adding_check_wish_is_displayed_2"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(2)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Проверяем вторым пользователем что подарок видно
            # main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
            # time.sleep(2)
            # main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
            # time.sleep(4)
            # main_page_1.swipe_up(600)
            #
            # # Screenshot block
            # action_taken = "_privacy_some_check_by_second_phone"
            # ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            # ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            # MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            # MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            # time.sleep(2)
            # assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Проверяем третьим пользователем что подарок НЕ видно
            # main_page_1.logout(self.driver)
            # main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend3, TestData.confirm_code)
            # main_page_1.register_new_user(self.driver, TestData.phone_friend2)
            # time.sleep(2)
            # main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
            # time.sleep(2)
            # main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
            # time.sleep(4)
            # main_page_1.swipe_up(600)

            # Screenshot block
            # action_taken = "_privacy_some_check_by_third_phone"
            # ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            # ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            # MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            # MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            # time.sleep(2)
            # assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

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

            # LAMODA

    @pytest.mark.side_wish_tests
    def test_add_custom_gift_visible_all_lamoda(self):
        """Создание желания с ссылкой на товар из маркетплейса Lamoda с областью видимости Доступно всем"""
        main_page_1 = MainPage(self.driver)

        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = ""
        test_ss_name = "custom_wish_from_lamoda_privacy_all"

        # Authenticate and delete users before the test
        auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend2)
        auth_controller.authenticate_and_register_user(TestData.phone_friend1, "Firsty", "11", "1111")
        auth_controller.authenticate_and_register_user(TestData.phone_friend2, "Vtoroy", "12", "1111")

        try:
            # Auth user 1
            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)

            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend2, TestData.confirm_code)
            main_page_1.register_new_user(self.driver, TestData.phone_friend2)
            main_page_1.logout(self.driver)
            main_page_1.auth_by_phone(TestData.phone_friend2, TestData.confirm_code)

            self.assertTrue(main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                            "Profile settings button not visible!")
            # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")
            self.assertTrue(main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                            "Profile settings button not visible!")
            # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")

            # Navigate to add custom gift
            main_page_1.click(MainPage.GIFT_LIST_LOCATOR)
            # TelegramReport.send_tg("click(MainPage.GIFT_LIST_LOCATOR)")
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

            main_page_1.send_keys(MainPage.ADD_CUSTOM_WISH_LINK, TestData.parseLamoda)
            # TelegramReport.send_tg("send_keys(TestData.parseLamoda)")
            time.sleep(2)

            # Finalize custom gift addition
            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")

            time.sleep(40)

            # Screenshot block
            action_taken = "_custom_wish_added_parsed_text_fields"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")
            time.sleep(4)

            # Screenshot block
            action_taken = "_custom_wish_added_parsed_photos"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")
            time.sleep(2)

            main_page_1.click(MainPage.DONE_BUTTON)
            # TelegramReport.send_tg("click(MainPage.DONE_BUTTON)")

            main_page_1.click(TestData.BOTTOM_WISHES_BTN)
            # TelegramReport.send_tg("click(MainPage.WISHMY)")
            time.sleep(3)

            # Screenshot block
            action_taken = "_custom_wish_after_adding_check_wish_is_displayed"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(2)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Проверяем вторым пользователем что подарок видно
            main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
            time.sleep(2)
            main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
            time.sleep(4)

            # Screenshot block
            action_taken = "_privacy_all_check_by_second_phone"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(2)
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

    @pytest.mark.side_wish_tests
    def test_add_custom_gift_visible_only_me_lamoda(self):
        """Создание желания с ссылкой на товар из маркетплейса Lamoda с областью видимости Доступно Только мне"""
        main_page_1 = MainPage(self.driver)

        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = ""
        test_ss_name = "custom_wish_from_lamoda_privacy_only_me"

        # Authenticate and delete users before the test
        auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend2)
        auth_controller.authenticate_and_register_user(TestData.phone_friend1, "Firsty", "11", "1111")
        auth_controller.authenticate_and_register_user(TestData.phone_friend2, "Vtoroy", "12", "1111")

        try:
            # Auth user 1
            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)

            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend2, TestData.confirm_code)
            main_page_1.register_new_user(self.driver, TestData.phone_friend2)
            main_page_1.logout(self.driver)
            main_page_1.auth_by_phone(TestData.phone_friend2, TestData.confirm_code)

            self.assertTrue(main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                            "Profile settings button not visible!")
            # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")
            self.assertTrue(main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                            "Profile settings button not visible!")
            # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")

            # Navigate to add custom gift
            main_page_1.click(MainPage.GIFT_LIST_LOCATOR)
            # TelegramReport.send_tg("click(MainPage.GIFT_LIST_LOCATOR)")
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

            main_page_1.send_keys(MainPage.ADD_CUSTOM_WISH_LINK, TestData.parseLamoda)
            # TelegramReport.send_tg("send_keys(TestData.parseLamoda)")
            time.sleep(2)

            # Добавили ссылку, жмем далее
            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")

            time.sleep(40)

            # Screenshot block
            action_taken = "_custom_wish_added_parsed_text_fields"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Дождались загрузки результата парсера, жмем далее
            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")
            time.sleep(4)

            # Screenshot block
            action_taken = "_custom_wish_added_parsed_photos"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Дождались загрузки фоток с парсера, жмем далее
            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")
            time.sleep(2)

            # Выбираем приватность
            main_page_1.click_by_uiautomator_desc_contains(MainPage.PRIVACY_ONLY_ME_DESC)
            # TelegramReport.send_tg("click(MainPage.PRIVACY_ONLY_ME_BOUNDS)")

            # Выбрали приватность, жмем Готово
            main_page_1.click(MainPage.DONE_BUTTON)
            time.sleep(3)

            main_page_1.click(TestData.BOTTOM_WISHES_BTN)
            # TelegramReport.send_tg("click(MainPage.WISHMY)")
            time.sleep(3)

            # Screenshot block
            action_taken = "_custom_wish_after_adding_check_wish_is_displayed"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(2)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Проверяем вторым пользователем что подарок видно
            main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
            time.sleep(2)
            main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
            time.sleep(4)
            main_page_1.swipe_up(600)

            # Screenshot block
            action_taken = "_privacy_all_check_by_second_phone"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(2)
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

    @pytest.mark.side_wish_tests
    def test_add_custom_gift_visible_some_lamoda(self):
        """Создание желания с ссылкой на товар из маркетплейса Lamoda с областью видимости Доступно Некоторым"""
        main_page_1 = MainPage(self.driver)

        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = ""
        test_ss_name = "test_add_custom_gift_visible_some_lamoda"

        # Authenticate and delete users before the test
        auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend2)
        auth_controller.authenticate_and_register_user(TestData.phone_friend1, "Firsty", "11", "1111")
        auth_controller.authenticate_and_register_user(TestData.phone_friend2, "Vtoroy", "12", "1111")
        auth_controller.authenticate_and_delete_user(TestData.phone_friend3)

        try:
            # Auth user 1
            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)

            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend2, TestData.confirm_code)
            main_page_1.register_new_user(self.driver, TestData.phone_friend2)
            main_page_1.logout(self.driver)
            main_page_1.auth_by_phone(TestData.phone_friend2, TestData.confirm_code)

            self.assertTrue(main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                            "Profile settings button not visible!")
            # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")
            self.assertTrue(main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                            "Profile settings button not visible!")
            # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")

            # Navigate to add custom gift
            main_page_1.click(MainPage.GIFT_LIST_LOCATOR)
            # TelegramReport.send_tg("click(MainPage.GIFT_LIST_LOCATOR)")
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

            main_page_1.send_keys(MainPage.ADD_CUSTOM_WISH_LINK, TestData.parseLamoda)
            # TelegramReport.send_tg("send_keys(TestData.parseLamoda)")
            time.sleep(2)

            # Добавили ссылку, жмем далее
            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")

            time.sleep(40)

            # Screenshot block
            action_taken = "_custom_wish_added_parsed_text_fields"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Дождались загрузки результата парсера, жмем далее
            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")
            time.sleep(4)

            # Screenshot block
            action_taken = "_custom_wish_added_parsed_photos"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Дождались загрузки фоток с парсера, жмем далее
            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")
            time.sleep(2)

            # Выбираем приватность
            main_page_1.click_by_uiautomator_desc_contains(MainPage.PRIVACY_SOME_DESC)
            time.sleep(2)
            # TelegramReport.send_tg("click(MainPage.PRIVACY_SOME)")

            # Выбрали приватность, жмем Готово
            main_page_1.click(MainPage.DONE_BUTTON)
            time.sleep(3)

            # Выбираем друга TODO ждем бага пока починят выбор
            main_page_1.click_by_uiautomator_desc_contains(TestData.choose_friends_first)
            time.sleep(1)

            # Выбрали друга, жмем Готово
            main_page_1.click(MainPage.DONE_BUTTON)
            # TelegramReport.send_tg("click(MainPage.DONE_BUTTON)")

            # Проверяем что подарок добавлен
            main_page_1.click(TestData.BOTTOM_WISHES_BTN)
            # TelegramReport.send_tg("click(MainPage.WISHMY)")
            time.sleep(3)

            # Screenshot block
            action_taken = "_custom_wish_after_adding_check_wish_is_displayed"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(2)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Проверяем вторым пользователем что подарок видно
            main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
            time.sleep(2)
            main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
            time.sleep(4)
            main_page_1.swipe_up(600)

            # Screenshot block
            action_taken = "_privacy_some_check_by_second_phone"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(2)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Проверяем третьим пользователем что подарок НЕ видно
            main_page_1.logout(self.driver)
            main_page_1.auth_by_phone(TestData.phone_friend3, TestData.confirm_code)
            main_page_1.register_new_user(self.driver, TestData.phone_friend2)
            time.sleep(2)
            main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
            time.sleep(2)
            main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
            time.sleep(4)
            main_page_1.swipe_up(600)

            # Screenshot block
            action_taken = "_privacy_some_check_by_third_phone"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(2)
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

    @pytest.mark.side_wish_tests
    def test_add_custom_gift_with_edit_and_visible_some_lamoda(self):
        """Создание желания с ссылкой на товар из маркетплейса Lamoda, редактированием спарсенных полей и с областью видимости Доступно Некоторым"""
        main_page_1 = MainPage(self.driver)

        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = ""
        test_ss_name = "test_add_custom_gift_with_edit_and_visible_some_lamoda"

        # Authenticate and delete users before the test
        auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend2)
        auth_controller.authenticate_and_register_user(TestData.phone_friend1, "Firsty", "11", "1111")
        auth_controller.authenticate_and_register_user(TestData.phone_friend2, "Vtoroy", "12", "1111")
        auth_controller.authenticate_and_delete_user(TestData.phone_friend3)

        try:
            # Auth user 1
            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)

            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend2, TestData.confirm_code)
            main_page_1.register_new_user(self.driver, TestData.phone_friend2)
            main_page_1.logout(self.driver)
            main_page_1.auth_by_phone(TestData.phone_friend2, TestData.confirm_code)

            self.assertTrue(main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                            "Profile settings button not visible!")
            # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")
            self.assertTrue(main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                            "Profile settings button not visible!")
            # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")

            # Navigate to add custom gift
            main_page_1.click(MainPage.GIFT_LIST_LOCATOR)
            # TelegramReport.send_tg("click(MainPage.GIFT_LIST_LOCATOR)")
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

            main_page_1.send_keys(MainPage.ADD_CUSTOM_WISH_LINK, TestData.parseLamoda)
            # TelegramReport.send_tg("send_keys(TestData.parseLamoda)")
            time.sleep(2)

            # Добавили ссылку, жмем далее
            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")

            time.sleep(40)

            # Дождались парсера, редактируем данные
            # Поле Имя
            main_page_1.click_element_by_bounds(TestData.custom_wish_name_field)
            time.sleep(1)
            main_page_1.clear_text_field_simple(self.driver)
            time.sleep(1)
            main_page_1.send_keys_simple("Test Name Of Wish Customized")
            time.sleep(1)
            # Поле Стоимость
            main_page_1.click_element_by_bounds(TestData.custom_wish_price_field)
            time.sleep(1)
            main_page_1.clear_text_field_simple(self.driver)
            time.sleep(1)
            main_page_1.send_keys_simple("5555")
            time.sleep(1)
            # Поле Описание
            main_page_1.click_element_by_bounds(TestData.custom_wish_description_field)
            time.sleep(1)
            main_page_1.clear_text_field_simple(self.driver)
            time.sleep(1)
            main_page_1.send_keys_simple("custom wish description not so long")
            time.sleep(1)

            # Screenshot того как было заполнено желание
            action_taken = "_custom_wish_edited_parsed_text_fields"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Дождались загрузки результата парсера, жмем далее
            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")
            time.sleep(4)

            # Screenshot block
            action_taken = "_custom_wish_added_parsed_photos"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Дождались загрузки фоток с парсера, жмем далее
            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")
            time.sleep(2)

            # Выбираем приватность
            # main_page_1.click_by_uiautomator_desc_contains(MainPage.PRIVACY_SOME_DESC) TODO
            # main_page_1.click_element_by_bounds(MainPage.PRIVACY_ALL)
            time.sleep(2)
            # TelegramReport.send_tg("click(MainPage.PRIVACY_SOME)")

            # Выбрали приватность, жмем Готово
            main_page_1.click(MainPage.DONE_BUTTON)
            time.sleep(3)

            # Выбираем друга TODO ждем бага пока починят выбор
            # main_page_1.click_by_uiautomator_desc_contains(TestData.choose_friends_first)
            time.sleep(1)

            # Выбрали друга, жмем Готово
            # main_page_1.click(MainPage.DONE_BUTTON) TODO
            # TelegramReport.send_tg("click(MainPage.DONE_BUTTON)")

            # Проверяем что подарок добавлен и видно кастомные поля
            main_page_1.click(TestData.BOTTOM_WISHES_BTN)
            # TelegramReport.send_tg("click(MainPage.WISHMY)")
            time.sleep(3)
            main_page_1.click_by_uiautomator(TestData.MY_WISHES_FIRST_WISH)
            time.sleep(3)
            # Screenshot после открытия подарка
            action_taken = "_custom_wish_after_adding_check_wish_is_displayed"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(2)
            # Compare screenshots and assert result
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Скроллим вниз чтобы увидеть описание товара
            main_page_1.swipe_up(1300)
            time.sleep(2)

            # Screenshot block
            action_taken = "_custom_wish_after_adding_check_wish_is_displayed_2"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(2)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Проверяем вторым пользователем что подарок видно
            # main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
            # time.sleep(2)
            # main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
            # time.sleep(4)
            # main_page_1.swipe_up(600)
            #
            # # Screenshot block
            # action_taken = "_privacy_some_check_by_second_phone"
            # ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            # ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            # MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            # MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            # time.sleep(2)
            # assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Проверяем третьим пользователем что подарок НЕ видно
            # main_page_1.logout(self.driver)
            # main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend3, TestData.confirm_code)
            # main_page_1.register_new_user(self.driver, TestData.phone_friend2)
            # time.sleep(2)
            # main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
            # time.sleep(2)
            # main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
            # time.sleep(4)
            # main_page_1.swipe_up(600)

            # Screenshot block
            # action_taken = "_privacy_some_check_by_third_phone"
            # ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            # ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            # MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            # MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            # time.sleep(2)
            # assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

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

            # MEGAMARKET

    @pytest.mark.side_wish_tests
    def test_add_custom_gift_visible_all_megamarket(self):
        """Создание желания с ссылкой на товар из маркетплейса Megamarket с областью видимости Доступно всем"""
        main_page_1 = MainPage(self.driver)

        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = ""
        test_ss_name = "custom_wish_from_megamarket_privacy_all"

        # Authenticate and delete users before the test
        auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend2)
        auth_controller.authenticate_and_register_user(TestData.phone_friend1, "Firsty", "11", "1111")
        auth_controller.authenticate_and_register_user(TestData.phone_friend2, "Vtoroy", "12", "1111")

        try:
            # Auth user 1
            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)

            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend2, TestData.confirm_code)
            main_page_1.register_new_user(self.driver, TestData.phone_friend2)
            main_page_1.logout(self.driver)
            main_page_1.auth_by_phone(TestData.phone_friend2, TestData.confirm_code)

            self.assertTrue(main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                            "Profile settings button not visible!")
            # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")
            self.assertTrue(main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                            "Profile settings button not visible!")
            # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")

            # Navigate to add custom gift
            main_page_1.click(MainPage.GIFT_LIST_LOCATOR)
            # TelegramReport.send_tg("click(MainPage.GIFT_LIST_LOCATOR)")
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

            main_page_1.send_keys(MainPage.ADD_CUSTOM_WISH_LINK, TestData.parseMegamarket)
            # TelegramReport.send_tg("send_keys(TestData.parseMegamarket)")
            time.sleep(2)

            # Finalize custom gift addition
            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")

            time.sleep(40)

            # Screenshot block
            action_taken = "_custom_wish_added_parsed_text_fields"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")
            time.sleep(4)

            # Screenshot block
            action_taken = "_custom_wish_added_parsed_photos"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")
            time.sleep(2)

            main_page_1.click(MainPage.DONE_BUTTON)
            # TelegramReport.send_tg("click(MainPage.DONE_BUTTON)")

            main_page_1.click(TestData.BOTTOM_WISHES_BTN)
            # TelegramReport.send_tg("click(MainPage.WISHMY)")
            time.sleep(3)

            # Screenshot block
            action_taken = "_custom_wish_after_adding_check_wish_is_displayed"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(2)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Проверяем вторым пользователем что подарок видно
            main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
            time.sleep(2)
            main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
            time.sleep(4)

            # Screenshot block
            action_taken = "_privacy_all_check_by_second_phone"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(2)
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

    @pytest.mark.side_wish_tests
    def test_add_custom_gift_visible_only_me_megamarket(self):
        """Создание желания с ссылкой на товар из маркетплейса Megamarket с областью видимости Доступно Только мне"""
        main_page_1 = MainPage(self.driver)

        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = ""
        test_ss_name = "custom_wish_from_megamarket_privacy_only_me"

        # Authenticate and delete users before the test
        auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend2)
        auth_controller.authenticate_and_register_user(TestData.phone_friend1, "Firsty", "11", "1111")
        auth_controller.authenticate_and_register_user(TestData.phone_friend2, "Vtoroy", "12", "1111")

        try:
            # Auth user 1
            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)

            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend2, TestData.confirm_code)
            main_page_1.register_new_user(self.driver, TestData.phone_friend2)
            main_page_1.logout(self.driver)
            main_page_1.auth_by_phone(TestData.phone_friend2, TestData.confirm_code)

            self.assertTrue(main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                            "Profile settings button not visible!")
            # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")
            self.assertTrue(main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                            "Profile settings button not visible!")
            # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")

            # Navigate to add custom gift
            main_page_1.click(MainPage.GIFT_LIST_LOCATOR)
            # TelegramReport.send_tg("click(MainPage.GIFT_LIST_LOCATOR)")
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

            main_page_1.send_keys(MainPage.ADD_CUSTOM_WISH_LINK, TestData.parseMegamarket)
            # TelegramReport.send_tg("send_keys(TestData.parseMegamarket)")
            time.sleep(2)

            # Добавили ссылку, жмем далее
            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")

            time.sleep(40)

            # Screenshot block
            action_taken = "_custom_wish_added_parsed_text_fields"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Дождались загрузки результата парсера, жмем далее
            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")
            time.sleep(4)

            # Screenshot block
            action_taken = "_custom_wish_added_parsed_photos"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Дождались загрузки фоток с парсера, жмем далее
            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")
            time.sleep(2)

            # Выбираем приватность
            main_page_1.click_by_uiautomator_desc_contains(MainPage.PRIVACY_ONLY_ME_DESC)
            # TelegramReport.send_tg("click(MainPage.PRIVACY_ONLY_ME_BOUNDS)")

            # Выбрали приватность, жмем Готово
            main_page_1.click(MainPage.DONE_BUTTON)
            time.sleep(3)

            main_page_1.click(TestData.BOTTOM_WISHES_BTN)
            # TelegramReport.send_tg("click(MainPage.WISHMY)")
            time.sleep(3)

            # Screenshot block
            action_taken = "_custom_wish_after_adding_check_wish_is_displayed"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(2)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Проверяем вторым пользователем что подарок видно
            main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
            time.sleep(2)
            main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
            time.sleep(4)
            main_page_1.swipe_up(600)

            # Screenshot block
            action_taken = "_privacy_all_check_by_second_phone"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(2)
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

    @pytest.mark.side_wish_tests
    def test_add_custom_gift_visible_some_megamarket(self):
        """Создание желания с ссылкой на товар из маркетплейса Megamarket с областью видимости Доступно Некоторым"""
        main_page_1 = MainPage(self.driver)

        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = ""
        test_ss_name = "test_add_custom_gift_visible_some_megamarket"

        # Authenticate and delete users before the test
        auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend2)
        auth_controller.authenticate_and_register_user(TestData.phone_friend1, "Firsty", "11", "1111")
        auth_controller.authenticate_and_register_user(TestData.phone_friend2, "Vtoroy", "12", "1111")
        auth_controller.authenticate_and_delete_user(TestData.phone_friend3)

        try:
            # Auth user 1
            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)

            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend2, TestData.confirm_code)
            main_page_1.register_new_user(self.driver, TestData.phone_friend2)
            main_page_1.logout(self.driver)
            main_page_1.auth_by_phone(TestData.phone_friend2, TestData.confirm_code)

            self.assertTrue(main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                            "Profile settings button not visible!")
            # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")
            self.assertTrue(main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                            "Profile settings button not visible!")
            # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")

            # Navigate to add custom gift
            main_page_1.click(MainPage.GIFT_LIST_LOCATOR)
            # TelegramReport.send_tg("click(MainPage.GIFT_LIST_LOCATOR)")
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

            main_page_1.send_keys(MainPage.ADD_CUSTOM_WISH_LINK, TestData.parseMegamarket)
            # TelegramReport.send_tg("send_keys(TestData.parseMegamarket)")
            time.sleep(2)

            # Добавили ссылку, жмем далее
            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")

            time.sleep(40)

            # Screenshot block
            action_taken = "_custom_wish_added_parsed_text_fields"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Дождались загрузки результата парсера, жмем далее
            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")
            time.sleep(4)

            # Screenshot block
            action_taken = "_custom_wish_added_parsed_photos"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Дождались загрузки фоток с парсера, жмем далее
            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")
            time.sleep(2)

            # Выбираем приватность
            main_page_1.click_by_uiautomator_desc_contains(MainPage.PRIVACY_SOME_DESC)
            time.sleep(2)
            # TelegramReport.send_tg("click(MainPage.PRIVACY_SOME)")

            # Выбрали приватность, жмем Готово
            main_page_1.click(MainPage.DONE_BUTTON)
            time.sleep(3)

            # Выбираем друга TODO ждем бага пока починят выбор
            main_page_1.click_by_uiautomator_desc_contains(TestData.choose_friends_first)
            time.sleep(1)

            # Выбрали друга, жмем Готово
            main_page_1.click(MainPage.DONE_BUTTON)
            # TelegramReport.send_tg("click(MainPage.DONE_BUTTON)")

            # Проверяем что подарок добавлен
            main_page_1.click(TestData.BOTTOM_WISHES_BTN)
            # TelegramReport.send_tg("click(MainPage.WISHMY)")
            time.sleep(3)

            # Screenshot block
            action_taken = "_custom_wish_after_adding_check_wish_is_displayed"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(2)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Проверяем вторым пользователем что подарок видно
            main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
            time.sleep(2)
            main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
            time.sleep(4)
            main_page_1.swipe_up(600)

            # Screenshot block
            action_taken = "_privacy_some_check_by_second_phone"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(2)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Проверяем третьим пользователем что подарок НЕ видно
            main_page_1.logout(self.driver)
            main_page_1.auth_by_phone(TestData.phone_friend3, TestData.confirm_code)
            main_page_1.register_new_user(self.driver, TestData.phone_friend2)
            time.sleep(2)
            main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
            time.sleep(2)
            main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
            time.sleep(4)
            main_page_1.swipe_up(600)

            # Screenshot block
            action_taken = "_privacy_some_check_by_third_phone"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(2)
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

    @pytest.mark.side_wish_tests
    def test_add_custom_gift_with_edit_and_visible_some_megamarket(self):
        """Создание желания с ссылкой на товар из маркетплейса Megamarket, редактированием спарсенных полей и с областью видимости Доступно Некоторым"""
        main_page_1 = MainPage(self.driver)

        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = ""
        test_ss_name = "test_add_custom_gift_with_edit_and_visible_some_megamarket"

        # Authenticate and delete users before the test
        auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend2)
        auth_controller.authenticate_and_register_user(TestData.phone_friend1, "Firsty", "11", "1111")
        auth_controller.authenticate_and_register_user(TestData.phone_friend2, "Vtoroy", "12", "1111")
        auth_controller.authenticate_and_delete_user(TestData.phone_friend3)

        try:
            # Auth user 1
            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)

            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend2, TestData.confirm_code)
            main_page_1.register_new_user(self.driver, TestData.phone_friend2)
            main_page_1.logout(self.driver)
            main_page_1.auth_by_phone(TestData.phone_friend2, TestData.confirm_code)

            self.assertTrue(main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                            "Profile settings button not visible!")
            # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")
            self.assertTrue(main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                            "Profile settings button not visible!")
            # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")

            # Navigate to add custom gift
            main_page_1.click(MainPage.GIFT_LIST_LOCATOR)
            # TelegramReport.send_tg("click(MainPage.GIFT_LIST_LOCATOR)")
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

            main_page_1.send_keys(MainPage.ADD_CUSTOM_WISH_LINK, TestData.parseMegamarket)
            # TelegramReport.send_tg("send_keys(TestData.parseMegamarket)")
            time.sleep(2)

            # Добавили ссылку, жмем далее
            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")

            time.sleep(40)

            # Дождались парсера, редактируем данные
            # Поле Имя
            main_page_1.click_element_by_bounds(TestData.custom_wish_name_field)
            time.sleep(1)
            main_page_1.clear_text_field_simple(self.driver)
            time.sleep(1)
            main_page_1.send_keys_simple("Test Name Of Wish Customized")
            time.sleep(1)
            # Поле Стоимость
            main_page_1.click_element_by_bounds(TestData.custom_wish_price_field)
            time.sleep(1)
            main_page_1.clear_text_field_simple(self.driver)
            time.sleep(1)
            main_page_1.send_keys_simple("5555")
            time.sleep(1)
            # Поле Описание
            main_page_1.click_element_by_bounds(TestData.custom_wish_description_field)
            time.sleep(1)
            main_page_1.clear_text_field_simple(self.driver)
            time.sleep(1)
            main_page_1.send_keys_simple("custom wish description not so long")
            time.sleep(1)

            # Screenshot того как было заполнено желание
            action_taken = "_custom_wish_edited_parsed_text_fields"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Дождались загрузки результата парсера, жмем далее
            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")
            time.sleep(4)

            # Screenshot block
            action_taken = "_custom_wish_added_parsed_photos"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Дождались загрузки фоток с парсера, жмем далее
            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")
            time.sleep(2)

            # Выбираем приватность
            # main_page_1.click_by_uiautomator_desc_contains(MainPage.PRIVACY_SOME_DESC) TODO
            # main_page_1.click_element_by_bounds(MainPage.PRIVACY_ALL)
            time.sleep(2)
            # TelegramReport.send_tg("click(MainPage.PRIVACY_SOME)")

            # Выбрали приватность, жмем Готово
            main_page_1.click(MainPage.DONE_BUTTON)
            time.sleep(3)

            # Выбираем друга TODO ждем бага пока починят выбор
            # main_page_1.click_by_uiautomator_desc_contains(TestData.choose_friends_first)
            time.sleep(1)

            # Выбрали друга, жмем Готово
            # main_page_1.click(MainPage.DONE_BUTTON) TODO
            # TelegramReport.send_tg("click(MainPage.DONE_BUTTON)")

            # Проверяем что подарок добавлен и видно кастомные поля
            main_page_1.click(TestData.BOTTOM_WISHES_BTN)
            # TelegramReport.send_tg("click(MainPage.WISHMY)")
            time.sleep(3)
            main_page_1.click_by_uiautomator(TestData.MY_WISHES_FIRST_WISH)
            time.sleep(3)
            # Screenshot после открытия подарка
            action_taken = "_custom_wish_after_adding_check_wish_is_displayed"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(2)
            # Compare screenshots and assert result
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Скроллим вниз чтобы увидеть описание товара
            main_page_1.swipe_up(1300)
            time.sleep(2)

            # Screenshot block
            action_taken = "_custom_wish_after_adding_check_wish_is_displayed_2"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(2)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Проверяем вторым пользователем что подарок видно
            # main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
            # time.sleep(2)
            # main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
            # time.sleep(4)
            # main_page_1.swipe_up(600)
            #
            # # Screenshot block
            # action_taken = "_privacy_some_check_by_second_phone"
            # ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            # ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            # MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            # MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            # time.sleep(2)
            # assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Проверяем третьим пользователем что подарок НЕ видно
            # main_page_1.logout(self.driver)
            # main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend3, TestData.confirm_code)
            # main_page_1.register_new_user(self.driver, TestData.phone_friend2)
            # time.sleep(2)
            # main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
            # time.sleep(2)
            # main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
            # time.sleep(4)
            # main_page_1.swipe_up(600)

            # Screenshot block
            # action_taken = "_privacy_some_check_by_third_phone"
            # ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            # ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            # MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            # MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            # time.sleep(2)
            # assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

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

            # GOLD APPLE

    @pytest.mark.side_wish_tests
    def test_add_custom_gift_visible_all_goldapple(self):
        """Создание желания с ссылкой на товар из маркетплейса Goldapple с областью видимости Доступно всем"""
        main_page_1 = MainPage(self.driver)

        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = ""
        test_ss_name = "custom_wish_from_goldapple_privacy_all"

        # Authenticate and delete users before the test
        auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend2)
        auth_controller.authenticate_and_register_user(TestData.phone_friend1, "Firsty", "11", "1111")
        auth_controller.authenticate_and_register_user(TestData.phone_friend2, "Vtoroy", "12", "1111")

        try:
            # Auth user 1
            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)

            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend2, TestData.confirm_code)
            main_page_1.register_new_user(self.driver, TestData.phone_friend2)
            main_page_1.logout(self.driver)
            main_page_1.auth_by_phone(TestData.phone_friend2, TestData.confirm_code)

            self.assertTrue(main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                            "Profile settings button not visible!")
            # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")
            self.assertTrue(main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                            "Profile settings button not visible!")
            # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")

            # Navigate to add custom gift
            main_page_1.click(MainPage.GIFT_LIST_LOCATOR)
            # TelegramReport.send_tg("click(MainPage.GIFT_LIST_LOCATOR)")
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

            main_page_1.send_keys(MainPage.ADD_CUSTOM_WISH_LINK, TestData.parseGoldapple)
            # TelegramReport.send_tg("send_keys(TestData.parseGoldapple)")
            time.sleep(2)

            # Finalize custom gift addition
            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")

            time.sleep(40)

            # Screenshot block
            action_taken = "_custom_wish_added_parsed_text_fields"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")
            time.sleep(4)

            # Screenshot block
            action_taken = "_custom_wish_added_parsed_photos"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")
            time.sleep(2)

            main_page_1.click(MainPage.DONE_BUTTON)
            # TelegramReport.send_tg("click(MainPage.DONE_BUTTON)")

            main_page_1.click(TestData.BOTTOM_WISHES_BTN)
            # TelegramReport.send_tg("click(MainPage.WISHMY)")
            time.sleep(3)

            # Screenshot block
            action_taken = "_custom_wish_after_adding_check_wish_is_displayed"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(2)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Проверяем вторым пользователем что подарок видно
            main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
            time.sleep(2)
            main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
            time.sleep(4)

            # Screenshot block
            action_taken = "_privacy_all_check_by_second_phone"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(2)
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

    @pytest.mark.side_wish_tests
    def test_add_custom_gift_visible_only_me_goldapple(self):
        """Создание желания с ссылкой на товар из маркетплейса Goldapple с областью видимости Доступно Только мне"""
        main_page_1 = MainPage(self.driver)

        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = ""
        test_ss_name = "custom_wish_from_goldapple_privacy_only_me"

        # Authenticate and delete users before the test
        auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend2)
        auth_controller.authenticate_and_register_user(TestData.phone_friend1, "Firsty", "11", "1111")
        auth_controller.authenticate_and_register_user(TestData.phone_friend2, "Vtoroy", "12", "1111")

        try:
            # Auth user 1
            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)

            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend2, TestData.confirm_code)
            main_page_1.register_new_user(self.driver, TestData.phone_friend2)
            main_page_1.logout(self.driver)
            main_page_1.auth_by_phone(TestData.phone_friend2, TestData.confirm_code)

            self.assertTrue(main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                            "Profile settings button not visible!")
            # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")
            self.assertTrue(main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                            "Profile settings button not visible!")
            # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")

            # Navigate to add custom gift
            main_page_1.click(MainPage.GIFT_LIST_LOCATOR)
            # TelegramReport.send_tg("click(MainPage.GIFT_LIST_LOCATOR)")
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

            main_page_1.send_keys(MainPage.ADD_CUSTOM_WISH_LINK, TestData.parseGoldapple)
            # TelegramReport.send_tg("send_keys(TestData.parseGoldapple)")
            time.sleep(2)

            # Добавили ссылку, жмем далее
            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")

            time.sleep(40)

            # Screenshot block
            action_taken = "_custom_wish_added_parsed_text_fields"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Дождались загрузки результата парсера, жмем далее
            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")
            time.sleep(4)

            # Screenshot block
            action_taken = "_custom_wish_added_parsed_photos"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Дождались загрузки фоток с парсера, жмем далее
            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")
            time.sleep(2)

            # Выбираем приватность
            main_page_1.click_by_uiautomator_desc_contains(MainPage.PRIVACY_ONLY_ME_DESC)
            # TelegramReport.send_tg("click(MainPage.PRIVACY_ONLY_ME_BOUNDS)")

            # Выбрали приватность, жмем Готово
            main_page_1.click(MainPage.DONE_BUTTON)
            time.sleep(3)

            main_page_1.click(TestData.BOTTOM_WISHES_BTN)
            # TelegramReport.send_tg("click(MainPage.WISHMY)")
            time.sleep(3)

            # Screenshot block
            action_taken = "_custom_wish_after_adding_check_wish_is_displayed"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(2)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Проверяем вторым пользователем что подарок видно
            main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
            time.sleep(2)
            main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
            time.sleep(4)
            main_page_1.swipe_up(600)

            # Screenshot block
            action_taken = "_privacy_all_check_by_second_phone"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(2)
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

    @pytest.mark.side_wish_tests
    def test_add_custom_gift_visible_some_goldapple(self):
        """Создание желания с ссылкой на товар из маркетплейса Goldapple с областью видимости Доступно Некоторым"""
        main_page_1 = MainPage(self.driver)

        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = ""
        test_ss_name = "test_add_custom_gift_visible_some_goldapple"

        # Authenticate and delete users before the test
        auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend2)
        auth_controller.authenticate_and_register_user(TestData.phone_friend1, "Firsty", "11", "1111")
        auth_controller.authenticate_and_register_user(TestData.phone_friend2, "Vtoroy", "12", "1111")
        auth_controller.authenticate_and_delete_user(TestData.phone_friend3)
        auth_controller.authenticate_and_register_user(TestData.phone_friend3, TestData.friend3_name, "12", "1111")
        try:
            # Auth user 1
            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)

            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend2, TestData.confirm_code)
            main_page_1.register_new_user(self.driver, TestData.phone_friend2)
            main_page_1.logout(self.driver)
            main_page_1.auth_by_phone(TestData.phone_friend2, TestData.confirm_code)

            self.assertTrue(main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                            "Profile settings button not visible!")
            # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")
            self.assertTrue(main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                            "Profile settings button not visible!")
            # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")

            # Navigate to add custom gift
            main_page_1.click(MainPage.GIFT_LIST_LOCATOR)
            # TelegramReport.send_tg("click(MainPage.GIFT_LIST_LOCATOR)")
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

            main_page_1.send_keys(MainPage.ADD_CUSTOM_WISH_LINK, TestData.parseGoldapple)
            # TelegramReport.send_tg("send_keys(TestData.parseGoldapple)")
            time.sleep(2)

            # Добавили ссылку, жмем далее
            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")

            time.sleep(40)

            # Screenshot block
            action_taken = "_custom_wish_added_parsed_text_fields"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Дождались загрузки результата парсера, жмем далее
            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")
            time.sleep(4)

            # Screenshot block
            action_taken = "_custom_wish_added_parsed_photos"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Дождались загрузки фоток с парсера, жмем далее
            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")
            time.sleep(2)

            # Выбираем приватность
            main_page_1.click_by_uiautomator_desc_contains(MainPage.PRIVACY_SOME_DESC)
            time.sleep(2)
            # TelegramReport.send_tg("click(MainPage.PRIVACY_SOME)")

            # Выбрали приватность, жмем Готово
            main_page_1.click(MainPage.DONE_BUTTON)
            time.sleep(3)

            # Выбираем друга TODO ждем бага пока починят выбор
            main_page_1.click_by_uiautomator_desc_contains(TestData.choose_friends_first)
            time.sleep(1)

            # Выбрали друга, жмем Готово
            main_page_1.click(MainPage.DONE_BUTTON)
            # TelegramReport.send_tg("click(MainPage.DONE_BUTTON)")

            # Проверяем что подарок добавлен
            main_page_1.click(TestData.BOTTOM_WISHES_BTN)
            # TelegramReport.send_tg("click(MainPage.WISHMY)")
            time.sleep(3)

            # Screenshot block
            action_taken = "_custom_wish_after_adding_check_wish_is_displayed"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(2)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Проверяем вторым пользователем что подарок видно
            main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
            time.sleep(2)
            main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
            time.sleep(4)
            main_page_1.swipe_up(600)

            # Screenshot block
            action_taken = "_privacy_some_check_by_second_phone"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(2)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Проверяем третьим пользователем что подарок НЕ видно
            main_page_1.logout(self.driver)
            main_page_1.auth_by_phone(TestData.phone_friend3, TestData.confirm_code)
            main_page_1.register_new_user(self.driver, TestData.phone_friend2)
            time.sleep(2)
            main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
            time.sleep(2)
            main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
            time.sleep(4)
            main_page_1.swipe_up(600)

            # Screenshot block
            action_taken = "_privacy_some_check_by_third_phone"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(2)
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

    @pytest.mark.side_wish_tests
    def test_add_custom_gift_with_edit_and_visible_some_goldapple(self):
        """Создание желания с ссылкой на товар из маркетплейса Goldapple, редактированием спарсенных полей и с областью видимости Доступно Некоторым"""
        main_page_1 = MainPage(self.driver)

        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = ""
        test_ss_name = "test_add_custom_gift_with_edit_and_visible_some_goldapple"

        # Authenticate and delete users before the test
        auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend2)
        auth_controller.authenticate_and_register_user(TestData.phone_friend1, "Firsty", "11", "1111")
        auth_controller.authenticate_and_register_user(TestData.phone_friend2, "Vtoroy", "12", "1111")
        auth_controller.authenticate_and_delete_user(TestData.phone_friend3)
        auth_controller.authenticate_and_register_user(TestData.phone_friend3, TestData.friend3_name, "12", "1111")
        try:
            # Auth user 1
            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)

            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend2, TestData.confirm_code)
            main_page_1.register_new_user(self.driver, TestData.phone_friend2)
            main_page_1.logout(self.driver)
            main_page_1.auth_by_phone(TestData.phone_friend2, TestData.confirm_code)

            self.assertTrue(main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                            "Profile settings button not visible!")
            # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")
            self.assertTrue(main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                            "Profile settings button not visible!")
            # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")

            # Navigate to add custom gift
            main_page_1.click(MainPage.GIFT_LIST_LOCATOR)
            # TelegramReport.send_tg("click(MainPage.GIFT_LIST_LOCATOR)")
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

            main_page_1.send_keys(MainPage.ADD_CUSTOM_WISH_LINK, TestData.parseGoldapple)
            # TelegramReport.send_tg("send_keys(TestData.parseGoldapple)")
            time.sleep(2)

            # Добавили ссылку, жмем далее
            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")

            time.sleep(40)

            # Дождались парсера, редактируем данные
            # Поле Имя
            main_page_1.click_element_by_bounds(TestData.custom_wish_name_field)
            time.sleep(1)
            main_page_1.clear_text_field_simple(self.driver)
            time.sleep(1)
            main_page_1.send_keys_simple("Test Name Of Wish Customized")
            time.sleep(1)
            # Поле Стоимость
            main_page_1.click_element_by_bounds(TestData.custom_wish_price_field)
            time.sleep(1)
            main_page_1.clear_text_field_simple(self.driver)
            time.sleep(1)
            main_page_1.send_keys_simple("5555")
            time.sleep(1)
            # Поле Описание
            main_page_1.click_element_by_bounds(TestData.custom_wish_description_field)
            time.sleep(1)
            main_page_1.clear_text_field_simple(self.driver)
            time.sleep(1)
            main_page_1.send_keys_simple("custom wish description not so long")
            time.sleep(1)

            # Screenshot того как было заполнено желание
            action_taken = "_custom_wish_edited_parsed_text_fields"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Дождались загрузки результата парсера, жмем далее
            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")
            time.sleep(4)

            # Screenshot block
            action_taken = "_custom_wish_added_parsed_photos"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Дождались загрузки фоток с парсера, жмем далее
            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")
            time.sleep(2)

            # Выбираем приватность
            # main_page_1.click_by_uiautomator_desc_contains(MainPage.PRIVACY_SOME_DESC) TODO
            # main_page_1.click_element_by_bounds(MainPage.PRIVACY_ALL)
            time.sleep(2)
            # TelegramReport.send_tg("click(MainPage.PRIVACY_SOME)")

            # Выбрали приватность, жмем Готово
            main_page_1.click(MainPage.DONE_BUTTON)
            time.sleep(3)

            # Выбираем друга TODO ждем бага пока починят выбор
            # main_page_1.click_by_uiautomator_desc_contains(TestData.choose_friends_first)
            time.sleep(1)

            # Выбрали друга, жмем Готово
            # main_page_1.click(MainPage.DONE_BUTTON) TODO
            # TelegramReport.send_tg("click(MainPage.DONE_BUTTON)")

            # Проверяем что подарок добавлен и видно кастомные поля
            main_page_1.click(TestData.BOTTOM_WISHES_BTN)
            # TelegramReport.send_tg("click(MainPage.WISHMY)")
            time.sleep(3)
            main_page_1.click_by_uiautomator(TestData.MY_WISHES_FIRST_WISH)
            time.sleep(3)
            # Screenshot после открытия подарка
            action_taken = "_custom_wish_after_adding_check_wish_is_displayed"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(2)
            # Compare screenshots and assert result
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Скроллим вниз чтобы увидеть описание товара
            main_page_1.swipe_up(1300)
            time.sleep(2)

            # Screenshot block
            action_taken = "_custom_wish_after_adding_check_wish_is_displayed_2"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(2)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Проверяем вторым пользователем что подарок видно
            # main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
            # time.sleep(2)
            # main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
            # time.sleep(4)
            # main_page_1.swipe_up(600)
            #
            # # Screenshot block
            # action_taken = "_privacy_some_check_by_second_phone"
            # ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            # ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            # MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            # MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            # time.sleep(2)
            # assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Проверяем третьим пользователем что подарок НЕ видно
            # main_page_1.logout(self.driver)
            # main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend3, TestData.confirm_code)
            # main_page_1.register_new_user(self.driver, TestData.phone_friend2)
            # time.sleep(2)
            # main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
            # time.sleep(2)
            # main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
            # time.sleep(4)
            # main_page_1.swipe_up(600)

            # Screenshot block
            # action_taken = "_privacy_some_check_by_third_phone"
            # ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            # ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            # MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            # MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            # time.sleep(2)
            # assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

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

            # OZON

    @pytest.mark.side_wish_tests
    def test_add_custom_gift_visible_all_ozon(self):
        """Создание желания с ссылкой на товар из маркетплейса Ozon с областью видимости Доступно всем"""
        main_page_1 = MainPage(self.driver)

        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = ""
        test_ss_name = "custom_wish_from_ozon_privacy_all"

        # Authenticate and delete users before the test
        auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend2)
        auth_controller.authenticate_and_register_user(TestData.phone_friend1, "Firsty", "11", "1111")
        auth_controller.authenticate_and_register_user(TestData.phone_friend2, "Vtoroy", "12", "1111")

        try:
            # Auth user 1
            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)

            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend2, TestData.confirm_code)
            main_page_1.register_new_user(self.driver, TestData.phone_friend2)
            main_page_1.logout(self.driver)
            main_page_1.auth_by_phone(TestData.phone_friend2, TestData.confirm_code)

            self.assertTrue(main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                            "Profile settings button not visible!")
            # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")
            self.assertTrue(main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                            "Profile settings button not visible!")
            # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")

            # Navigate to add custom gift
            main_page_1.click(MainPage.GIFT_LIST_LOCATOR)
            # TelegramReport.send_tg("click(MainPage.GIFT_LIST_LOCATOR)")
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

            main_page_1.send_keys(MainPage.ADD_CUSTOM_WISH_LINK, TestData.parseOzon)
            # TelegramReport.send_tg("send_keys(TestData.parseOzon)")
            time.sleep(2)

            # Finalize custom gift addition
            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")

            time.sleep(40)

            # Screenshot block
            action_taken = "_custom_wish_added_parsed_text_fields"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")
            time.sleep(4)

            # Screenshot block
            action_taken = "_custom_wish_added_parsed_photos"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")
            time.sleep(2)

            main_page_1.click(MainPage.DONE_BUTTON)
            # TelegramReport.send_tg("click(MainPage.DONE_BUTTON)")

            main_page_1.click(TestData.BOTTOM_WISHES_BTN)
            # TelegramReport.send_tg("click(MainPage.WISHMY)")
            time.sleep(3)

            # Screenshot block
            action_taken = "_custom_wish_after_adding_check_wish_is_displayed"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(2)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Проверяем вторым пользователем что подарок видно
            main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
            time.sleep(2)
            main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
            time.sleep(4)

            # Screenshot block
            action_taken = "_privacy_all_check_by_second_phone"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(2)
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

    @pytest.mark.side_wish_tests
    def test_add_custom_gift_visible_only_me_ozon(self):
        """Создание желания с ссылкой на товар из маркетплейса Ozon с областью видимости Доступно Только мне"""
        main_page_1 = MainPage(self.driver)

        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = ""
        test_ss_name = "custom_wish_from_ozon_privacy_only_me"

        # Authenticate and delete users before the test
        auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend2)
        auth_controller.authenticate_and_register_user(TestData.phone_friend1, "Firsty", "11", "1111")
        auth_controller.authenticate_and_register_user(TestData.phone_friend2, "Vtoroy", "12", "1111")

        try:
            # Auth user 1
            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)

            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend2, TestData.confirm_code)
            main_page_1.register_new_user(self.driver, TestData.phone_friend2)
            main_page_1.logout(self.driver)
            main_page_1.auth_by_phone(TestData.phone_friend2, TestData.confirm_code)

            self.assertTrue(main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                            "Profile settings button not visible!")
            # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")
            self.assertTrue(main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                            "Profile settings button not visible!")
            # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")

            # Navigate to add custom gift
            main_page_1.click(MainPage.GIFT_LIST_LOCATOR)
            # TelegramReport.send_tg("click(MainPage.GIFT_LIST_LOCATOR)")
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

            main_page_1.send_keys(MainPage.ADD_CUSTOM_WISH_LINK, TestData.parseOzon)
            # TelegramReport.send_tg("send_keys(TestData.parseOzon)")
            time.sleep(2)

            # Добавили ссылку, жмем далее
            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")

            time.sleep(40)

            # Screenshot block
            action_taken = "_custom_wish_added_parsed_text_fields"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Дождались загрузки результата парсера, жмем далее
            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")
            time.sleep(4)

            # Screenshot block
            action_taken = "_custom_wish_added_parsed_photos"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Дождались загрузки фоток с парсера, жмем далее
            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")
            time.sleep(2)

            # Выбираем приватность
            main_page_1.click_by_uiautomator_desc_contains(MainPage.PRIVACY_ONLY_ME_DESC)
            # TelegramReport.send_tg("click(MainPage.PRIVACY_ONLY_ME_BOUNDS)")

            # Выбрали приватность, жмем Готово
            main_page_1.click(MainPage.DONE_BUTTON)
            time.sleep(3)

            main_page_1.click(TestData.BOTTOM_WISHES_BTN)
            # TelegramReport.send_tg("click(MainPage.WISHMY)")
            time.sleep(3)

            # Screenshot block
            action_taken = "_custom_wish_after_adding_check_wish_is_displayed"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(2)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Проверяем вторым пользователем что подарок видно
            main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
            time.sleep(2)
            main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
            time.sleep(4)
            main_page_1.swipe_up(600)

            # Screenshot block
            action_taken = "_privacy_all_check_by_second_phone"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(2)
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

    @pytest.mark.side_wish_tests
    def test_add_custom_gift_visible_some_ozon(self):
        """Создание желания с ссылкой на товар из маркетплейса Ozon с областью видимости Доступно Некоторым"""
        main_page_1 = MainPage(self.driver)

        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = ""
        test_ss_name = "test_add_custom_gift_visible_some_ozon"

        # Authenticate and delete users before the test
        auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend2)
        auth_controller.authenticate_and_register_user(TestData.phone_friend1, "Firsty", "11", "1111")
        auth_controller.authenticate_and_register_user(TestData.phone_friend2, "Vtoroy", "12", "1111")
        auth_controller.authenticate_and_delete_user(TestData.phone_friend3)
        auth_controller.authenticate_and_register_user(TestData.phone_friend3, TestData.friend3_name, "12", "1111")
        try:
            # Auth user 1
            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)

            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend2, TestData.confirm_code)
            main_page_1.register_new_user(self.driver, TestData.phone_friend2)
            main_page_1.logout(self.driver)
            main_page_1.auth_by_phone(TestData.phone_friend2, TestData.confirm_code)

            self.assertTrue(main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                            "Profile settings button not visible!")
            # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")
            self.assertTrue(main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                            "Profile settings button not visible!")
            # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")

            # Navigate to add custom gift
            main_page_1.click(MainPage.GIFT_LIST_LOCATOR)
            # TelegramReport.send_tg("click(MainPage.GIFT_LIST_LOCATOR)")
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

            main_page_1.send_keys(MainPage.ADD_CUSTOM_WISH_LINK, TestData.parseOzon)
            # TelegramReport.send_tg("send_keys(TestData.parseOzon)")
            time.sleep(2)

            # Добавили ссылку, жмем далее
            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")

            time.sleep(40)

            # Screenshot block
            action_taken = "_custom_wish_added_parsed_text_fields"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Дождались загрузки результата парсера, жмем далее
            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")
            time.sleep(4)

            # Screenshot block
            action_taken = "_custom_wish_added_parsed_photos"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Дождались загрузки фоток с парсера, жмем далее
            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")
            time.sleep(2)

            # Выбираем приватность
            main_page_1.click_by_uiautomator_desc_contains(MainPage.PRIVACY_SOME_DESC)
            time.sleep(2)
            # TelegramReport.send_tg("click(MainPage.PRIVACY_SOME)")

            # Выбрали приватность, жмем Готово
            main_page_1.click(MainPage.DONE_BUTTON)
            time.sleep(3)

            # Выбираем друга TODO ждем бага пока починят выбор
            main_page_1.click_by_uiautomator_desc_contains(TestData.choose_friends_first)
            time.sleep(1)

            # Выбрали друга, жмем Готово
            main_page_1.click(MainPage.DONE_BUTTON)
            # TelegramReport.send_tg("click(MainPage.DONE_BUTTON)")

            # Проверяем что подарок добавлен
            main_page_1.click(TestData.BOTTOM_WISHES_BTN)
            # TelegramReport.send_tg("click(MainPage.WISHMY)")
            time.sleep(3)

            # Screenshot block
            action_taken = "_custom_wish_after_adding_check_wish_is_displayed"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(2)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Проверяем вторым пользователем что подарок видно
            main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
            time.sleep(2)
            main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
            time.sleep(4)
            main_page_1.swipe_up(600)

            # Screenshot block
            action_taken = "_privacy_some_check_by_second_phone"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(2)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Проверяем третьим пользователем что подарок НЕ видно
            main_page_1.logout(self.driver)
            main_page_1.auth_by_phone(TestData.phone_friend3, TestData.confirm_code)
            main_page_1.register_new_user(self.driver, TestData.phone_friend2)
            time.sleep(2)
            main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
            time.sleep(2)
            main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
            time.sleep(4)
            main_page_1.swipe_up(600)

            # Screenshot block
            action_taken = "_privacy_some_check_by_third_phone"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(2)
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

    @pytest.mark.side_wish_tests
    def test_add_custom_gift_with_edit_and_visible_some_ozon(self):
        """Создание желания с ссылкой на товар из маркетплейса Ozon, редактированием спарсенных полей и с областью видимости Доступно Некоторым"""
        main_page_1 = MainPage(self.driver)

        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = ""
        test_ss_name = "test_add_custom_gift_with_edit_and_visible_some_ozon"

        # Authenticate and delete users before the test
        auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend2)
        auth_controller.authenticate_and_register_user(TestData.phone_friend1, "Firsty", "11", "1111")
        auth_controller.authenticate_and_register_user(TestData.phone_friend2, "Vtoroy", "12", "1111")
        auth_controller.authenticate_and_delete_user(TestData.phone_friend3)
        auth_controller.authenticate_and_register_user(TestData.phone_friend3, TestData.friend3_name, "12", "1111")
        try:
            # Auth user 1
            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)

            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend2, TestData.confirm_code)
            main_page_1.register_new_user(self.driver, TestData.phone_friend2)
            main_page_1.logout(self.driver)
            main_page_1.auth_by_phone(TestData.phone_friend2, TestData.confirm_code)

            self.assertTrue(main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                            "Profile settings button not visible!")
            # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")
            self.assertTrue(main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                            "Profile settings button not visible!")
            # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")

            # Navigate to add custom gift
            main_page_1.click(MainPage.GIFT_LIST_LOCATOR)
            # TelegramReport.send_tg("click(MainPage.GIFT_LIST_LOCATOR)")
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

            main_page_1.send_keys(MainPage.ADD_CUSTOM_WISH_LINK, TestData.parseOzon)
            # TelegramReport.send_tg("send_keys(TestData.parseOzon)")
            time.sleep(2)

            # Добавили ссылку, жмем далее
            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")

            time.sleep(40)

            # Дождались парсера, редактируем данные
            # Поле Имя
            main_page_1.click_element_by_bounds(TestData.custom_wish_name_field)
            time.sleep(1)
            main_page_1.clear_text_field_simple(self.driver)
            time.sleep(1)
            main_page_1.send_keys_simple("Test Name Of Wish Customized")
            time.sleep(1)
            # Поле Стоимость
            main_page_1.click_element_by_bounds(TestData.custom_wish_price_field)
            time.sleep(1)
            main_page_1.clear_text_field_simple(self.driver)
            time.sleep(1)
            main_page_1.send_keys_simple("5555")
            time.sleep(1)
            # Поле Описание
            main_page_1.click_element_by_bounds(TestData.custom_wish_description_field)
            time.sleep(1)
            main_page_1.clear_text_field_simple(self.driver)
            time.sleep(1)
            main_page_1.send_keys_simple("custom wish description not so long")
            time.sleep(1)

            # Screenshot того как было заполнено желание
            action_taken = "_custom_wish_edited_parsed_text_fields"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Дождались загрузки результата парсера, жмем далее
            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")
            time.sleep(4)

            # Screenshot block
            action_taken = "_custom_wish_added_parsed_photos"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Дождались загрузки фоток с парсера, жмем далее
            main_page_1.click(TestData.next_button)
            # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")
            time.sleep(2)

            # Выбираем приватность
            # main_page_1.click_by_uiautomator_desc_contains(MainPage.PRIVACY_SOME_DESC) TODO
            # main_page_1.click_element_by_bounds(MainPage.PRIVACY_ALL)
            time.sleep(2)
            # TelegramReport.send_tg("click(MainPage.PRIVACY_SOME)")

            # Выбрали приватность, жмем Готово
            main_page_1.click(MainPage.DONE_BUTTON)
            time.sleep(3)

            # Выбираем друга TODO ждем бага пока починят выбор
            # main_page_1.click_by_uiautomator_desc_contains(TestData.choose_friends_first)
            time.sleep(1)

            # Выбрали друга, жмем Готово
            # main_page_1.click(MainPage.DONE_BUTTON) TODO
            # TelegramReport.send_tg("click(MainPage.DONE_BUTTON)")

            # Проверяем что подарок добавлен и видно кастомные поля
            main_page_1.click(TestData.BOTTOM_WISHES_BTN)
            # TelegramReport.send_tg("click(MainPage.WISHMY)")
            time.sleep(3)
            main_page_1.click_by_uiautomator(TestData.MY_WISHES_FIRST_WISH)
            time.sleep(3)
            # Screenshot после открытия подарка
            action_taken = "_custom_wish_after_adding_check_wish_is_displayed"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(2)
            # Compare screenshots and assert result
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Скроллим вниз чтобы увидеть описание товара
            main_page_1.swipe_up(1300)
            time.sleep(2)

            # Screenshot block
            action_taken = "_custom_wish_after_adding_check_wish_is_displayed_2"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(2)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Проверяем вторым пользователем что подарок видно
            # main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
            # time.sleep(2)
            # main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
            # time.sleep(4)
            # main_page_1.swipe_up(600)
            #
            # # Screenshot block
            # action_taken = "_privacy_some_check_by_second_phone"
            # ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            # ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            # MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            # MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            # time.sleep(2)
            # assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Проверяем третьим пользователем что подарок НЕ видно
            # main_page_1.logout(self.driver)
            # main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend3, TestData.confirm_code)
            # main_page_1.register_new_user(self.driver, TestData.phone_friend2)
            # time.sleep(2)
            # main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
            # time.sleep(2)
            # main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
            # time.sleep(4)
            # main_page_1.swipe_up(600)

            # Screenshot block
            # action_taken = "_privacy_some_check_by_third_phone"
            # ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            # ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            # MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            # MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            # time.sleep(2)
            # assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

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
