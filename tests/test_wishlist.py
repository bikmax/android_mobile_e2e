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


class WishList(BaseTest):

    @pytest.mark.regress
    @pytest.mark.wishlist_tests
    def test_wishlist(self):
        """Тесты вишлиста"""

        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = "Вишлист: Тесты вишлиста, создание, редактирование имени и даты, удаление желания, добавление после удаления и удаление вишлиста"
        test_ss_name = "test_wishlist"
        main_page_1 = MainPage(self.driver)
        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        # Authenticate and delete users before the test
        auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        auth_controller.authenticate_and_register_user(TestData.phone_friend1, TestData.friend1_name, "11", "1111")

        try:
            # Auth
            time.sleep(20)
            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)

            assert main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR), \
                "Profile settings button not visible!"
            # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")

            main_page_1.add_two_wishes()
            main_page_1.add_one_wish()

            # Create wishlist 1
            time.sleep(2)
            main_page_1.click(TestData.BOTTOM_WISHES_BTN)
            time.sleep(3)
            main_page_1.click_by_uiautomator(TestData.MY_WISHES_WISHLIST_CREATE)
            time.sleep(2)
            main_page_1.click_by_uiautomator(TestData.MY_WISHES_WISHLIST_CREATE_NAME_FIELD)
            time.sleep(2)
            main_page_1.send_keys_simple("My wishlist 1")
            time.sleep(2)
            main_page_1.click_by_uiautomator(TestData.MY_WISHES_WISHLIST_EVENTDATE_FIELD)
            time.sleep(2)
            main_page_1.send_keys_simple("11112030")
            time.sleep(2)
            main_page_1.click(MainPage.NEXT_BUTTON)
            time.sleep(2)
            main_page_1.click_by_uiautomator(TestData.MY_WISHES_WISHLIST_ADD_WISH_1)
            time.sleep(2)
            main_page_1.click_by_uiautomator(TestData.MY_WISHES_WISHLIST_ADD_WISH_2)
            time.sleep(2)
            main_page_1.click(MainPage.DONE_BUTTON)

            # 2
            time.sleep(6)
            main_page_1.click_by_uiautomator(TestData.MY_WISHES_WISHLIST_CREATE)
            time.sleep(2)
            main_page_1.click_by_uiautomator(TestData.MY_WISHES_WISHLIST_CREATE_NAME_FIELD)
            time.sleep(2)
            main_page_1.send_keys_simple("My wishlist 2")
            time.sleep(2)
            main_page_1.click_by_uiautomator(TestData.MY_WISHES_WISHLIST_EVENTDATE_FIELD)
            time.sleep(2)
            main_page_1.send_keys_simple("11112036")
            time.sleep(2)
            main_page_1.click(MainPage.NEXT_BUTTON)
            time.sleep(2)
            main_page_1.click_by_uiautomator(TestData.MY_WISHES_WISHLIST_ADD_WISH_1)
            time.sleep(2)
            main_page_1.click_by_uiautomator(TestData.MY_WISHES_WISHLIST_ADD_WISH_2)
            time.sleep(2)
            main_page_1.click(MainPage.DONE_BUTTON)
            time.sleep(2)

            # Assert steps below
            # Screenshot block
            action_taken = "_wishlist_created"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            # Attach screenshots to Allure report
            with allure.step("Taking screenshot of the etalon"):
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
                allure.attach.file(ss_etalon, name="Etalon Screenshot", attachment_type=allure.attachment_type.PNG)
            with allure.step("Taking screenshot of the run result"):
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
                allure.attach.file(ss_run, name="Run Screenshot", attachment_type=allure.attachment_type.PNG)
            time.sleep(1)
            # Screenshot comparison and assertion
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # edit wishlist: update name and date
            time.sleep(2)
            main_page_1.click_by_uiautomator(TestData.MY_WISHES_WISHLIST_CHOOSE_1)
            time.sleep(2)
            main_page_1.click_by_uiautomator(TestData.MY_WISHES_WISHLIST_EDIT_BUTTON)
            time.sleep(2)
            main_page_1.click_by_uiautomator(TestData.MY_WISHES_WISHLIST_EDIT_NAME_FIELD)
            time.sleep(2)
            main_page_1.send_keys_simple("444")
            time.sleep(2)
            # main_page_1.click_by_uiautomator(TestData.MY_WISHES_WISHLIST_EDIT_EVENTDATE_FIELD) TODO
            # time.sleep(2)
            # main_page_1.send_keys_simple("11112030")
            time.sleep(2)
            main_page_1.click(MainPage.DONE_BUTTON)
            time.sleep(2)

            # Screenshot block
            action_taken = "_wishlist_updated"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            # Attach screenshots to Allure report
            with allure.step("Taking screenshot of the etalon"):
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
                allure.attach.file(ss_etalon, name="Etalon Screenshot", attachment_type=allure.attachment_type.PNG)
            with allure.step("Taking screenshot of the run result"):
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
                allure.attach.file(ss_run, name="Run Screenshot", attachment_type=allure.attachment_type.PNG)
            time.sleep(1)
            # Screenshot comparison and assertion
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # edit wishlist: delete wish
            time.sleep(2)
            main_page_1.click_by_uiautomator(TestData.MY_WISHES_WISHLIST_CHOOSE_1)
            time.sleep(2)
            main_page_1.click_by_uiautomator(TestData.MY_WISHES_WISHLIST_EDIT_BUTTON)
            time.sleep(2)
            main_page_1.click(TestData.MY_WISHES_WISHLIST_EDIT_REMOVE_WISH_1)
            time.sleep(2)
            main_page_1.click(MainPage.DONE_BUTTON)
            time.sleep(2)

            # Screenshot block
            action_taken = "_wishlist_updated_del1"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            # Attach screenshots to Allure report
            with allure.step("Taking screenshot of the etalon"):
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
                allure.attach.file(ss_etalon, name="Etalon Screenshot", attachment_type=allure.attachment_type.PNG)
            with allure.step("Taking screenshot of the run result"):
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
                allure.attach.file(ss_run, name="Run Screenshot", attachment_type=allure.attachment_type.PNG)
            time.sleep(1)
            # Screenshot comparison and assertion
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # edit wishlist: add wishes
            time.sleep(2)
            main_page_1.click_by_uiautomator(TestData.MY_WISHES_WISHLIST_CHOOSE_1)
            time.sleep(2)
            main_page_1.click_by_uiautomator(TestData.MY_WISHES_WISHLIST_EDIT_BUTTON)
            time.sleep(2)
            main_page_1.click(TestData.MY_WISHES_WISHLIST_EDIT_ADD_WISH)
            time.sleep(2)
            main_page_1.click(TestData.MY_WISHES_WISHLIST_ADD_WISH_3)
            time.sleep(2)
            main_page_1.click(MainPage.DONE_BUTTON)
            time.sleep(2)

            # Screenshot block
            action_taken = "_wishlist_updated"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            # Attach screenshots to Allure report
            with allure.step("Taking screenshot of the etalon"):
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
                allure.attach.file(ss_etalon, name="Etalon Screenshot", attachment_type=allure.attachment_type.PNG)
            with allure.step("Taking screenshot of the run result"):
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
                allure.attach.file(ss_run, name="Run Screenshot", attachment_type=allure.attachment_type.PNG)
            time.sleep(1)
            # Screenshot comparison and assertion
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # delete wishlist
            time.sleep(2)
            main_page_1.click_by_uiautomator(TestData.MY_WISHES_WISHLIST_CHOOSE_1)
            time.sleep(2)
            main_page_1.click_by_uiautomator(TestData.MY_WISHES_WISHLIST_EDIT_BUTTON)
            time.sleep(2)
            main_page_1.click(TestData.MY_WISHES_WISHLIST_EDIT_DELETE_WISHLIST)
            time.sleep(2)
            main_page_1.click(TestData.BOTTOM_CONFIRM_ACTION_BTN)
            time.sleep(4)

            # Screenshot block
            action_taken = "_wishlist_deleted"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            # Attach screenshots to Allure report
            with allure.step("Taking screenshot of the etalon"):
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
                allure.attach.file(ss_etalon, name="Etalon Screenshot", attachment_type=allure.attachment_type.PNG)
            with allure.step("Taking screenshot of the run result"):
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
                allure.attach.file(ss_run, name="Run Screenshot", attachment_type=allure.attachment_type.PNG)
            time.sleep(1)
            # Screenshot comparison and assertion
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
