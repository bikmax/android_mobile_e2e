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


class ReserveWish(BaseTest):

    @pytest.mark.regress
    @pytest.mark.reserve_wish_tests
    def test_reserve_custom_friend_gift(self):
        main_page_1 = MainPage(self.driver)

        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = "Исполнение стороннего желания друга"
        test_ss_name = "test_reserve_custom_friend_gift"

        # Authenticate and delete users before the test
        with allure.step("Аутентификация и удаление пользователей перед тестом"):
            auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
            auth_controller.authenticate_and_delete_user(TestData.phone_friend2)
            auth_controller.authenticate_and_register_user(TestData.phone_friend1, "Firsty", "11", "1111")
            auth_controller.authenticate_and_register_user(TestData.phone_friend2, "Vtoroy", "12", "1111")

        try:
            # Auth user 1
            with allure.step("Аутентификация первого пользователя"):
                main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)
                main_page_1.add_one_wish()
                time.sleep(2)
                main_page_1.is_element_visible(TestData.BOTTOM_HOME_BTN_XP)
                main_page_1.click(TestData.BOTTOM_HOME_BTN_XP)
                time.sleep(2)
                main_page_1.click(TestData.BOTTOM_WISHES_BTN)
                time.sleep(2)
                main_page_1.is_element_visible(MainPage.ADD_WISH_BUTTON)
                main_page_1.click(MainPage.ADD_WISH_BUTTON)
                time.sleep(2)
                main_page_1.is_element_visible(TestData.custom_wish_add_button)
                main_page_1.click(TestData.custom_wish_add_button)
                time.sleep(2)
                main_page_1.is_element_visible(MainPage.ADD_CUSTOM_WISH_LINK)
                main_page_1.click(MainPage.ADD_CUSTOM_WISH_LINK)
                time.sleep(2)
                main_page_1.send_keys(MainPage.ADD_CUSTOM_WISH_LINK, TestData.parseWildberries)
                time.sleep(2)

            # Finalize custom gift addition
            with allure.step("Завершение добавления пользовательского подарка"):
                main_page_1.click(TestData.next_button)
                time.sleep(40)
                main_page_1.click(TestData.next_button)
                time.sleep(4)
                main_page_1.click(TestData.next_button)
                time.sleep(4)
                main_page_1.click(MainPage.DONE_BUTTON)
                time.sleep(4)
                main_page_1.is_element_visible(TestData.BOTTOM_WISHES_BTN)
                main_page_1.click(TestData.BOTTOM_WISHES_BTN)
                time.sleep(3)

            # Проверяем вторым пользователем что подарок видно
            with allure.step("Проверка видимости подарка вторым пользователем"):
                main_page_1.logout(self.driver)
                time.sleep(2)
                main_page_1.auth_by_phone(TestData.phone_friend2, TestData.confirm_code)
                time.sleep(2)
                main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
                time.sleep(6)
                main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
                time.sleep(6)

            # RESERVE WISH
            with allure.step("Резервирование желания"):
                main_page_1.swipe_up(700)
                # main_page_1.scroll_until_visible(self, TestData.friend_wish_3_wish)
                main_page_1.click_by_uiautomator_desc_contains("ножей")
                time.sleep(5)
                main_page_1.scroll_until_visible(self.driver, MainPage.RESERVE_WISH_BUTTON)
                time.sleep(5)
                main_page_1.click(MainPage.RESERVE_WISH_BUTTON)
                time.sleep(2)
                main_page_1.click(MainPage.RESERVE_WISH_FINAL_BUTTON)
                time.sleep(2)

            # ACCEPT WISH PHONE1
            with allure.step("Принятие резервирования первым пользователем"):
                main_page_1.logout(self.driver)
                time.sleep(2)
                main_page_1.auth_by_phone(TestData.phone_friend1, TestData.confirm_code)
                time.sleep(2)
                main_page_1.click(TestData.BOTTOM_WISHES_BTN)
                time.sleep(2)
                main_page_1.is_element_visible(TestData.MY_WISHES_FIRST_WISH)
                main_page_1.click(TestData.MY_WISHES_FIRST_WISH)
                time.sleep(2)
                main_page_1.is_element_visible(MainPage.ACCEPT_RESERVED_WISH)
                main_page_1.click(MainPage.ACCEPT_RESERVED_WISH)
                time.sleep(2)
                main_page_1.click(MainPage.ACCEPT_RESERVED_WISH)
                time.sleep(2)

            with allure.step("Проверка отображения уведомления о принятии резервирования"):
                self.assertTrue(
                    main_page_1.is_element_visible(MainPage.NOTIFICATION_YOUR_RESERVED_WISH_DONE_AND_ARCHIVED),
                    "NOTIFICATION_WISH_SUGGESTED not visible!"
                )
                self.assertTrue(
                    main_page_1.is_element_invisible(MainPage.NOTIFICATION_YOUR_RESERVED_WISH_DONE_AND_ARCHIVED),
                    "NOTIFICATION_WISH_SUGGESTED not visible!"
                )

            # make wish available again
            with allure.step("Сделать желание доступным снова"):
                main_page_1.is_element_visible(TestData.BOTTOM_WISHES_BTN)
                main_page_1.click(TestData.BOTTOM_WISHES_BTN)
                time.sleep(2)
                main_page_1.is_element_visible(TestData.wishes_show_all_whishes)
                main_page_1.click(TestData.wishes_show_all_whishes)
                time.sleep(2)
                main_page_1.is_element_visible(TestData.wishes_all_wishes_first_wish)
                main_page_1.click(TestData.wishes_all_wishes_first_wish)
                time.sleep(2)
                main_page_1.scroll_until_visible(self.driver, MainPage.ADD_WISH_AGAIN_BUTTON)
                time.sleep(2)
                main_page_1.is_element_visible(MainPage.ADD_WISH_AGAIN_BUTTON)
                main_page_1.click(MainPage.ADD_WISH_AGAIN_BUTTON)
                time.sleep(2)
                main_page_1.is_element_visible(MainPage.ADD_WISH_AGAIN_FINAL_BUTTON)
                main_page_1.click(MainPage.ADD_WISH_AGAIN_FINAL_BUTTON)
            with allure.step("Проверка отображения уведомления о доступности желания снова"):
                self.assertTrue(
                    main_page_1.is_element_visible(MainPage.NOTIFICATION_RESERVED_WISH_AVAILABLE_AGAIN),
                    "NOTIFICATION_WISH_SUGGESTED not visible!"
                )
                self.assertTrue(
                    main_page_1.is_element_invisible(MainPage.NOTIFICATION_RESERVED_WISH_AVAILABLE_AGAIN),
                    "NOTIFICATION_WISH_SUGGESTED not visible!"
                )
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

    @pytest.mark.reserve_wish_tests
    @pytest.mark.regress
    def test_decline_reserve_wish(self):
        """Отклонить бронирование своего кастомного желания другом"""
        main_page_1 = MainPage(self.driver)
        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()
        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = "Отклонить бронирование своего кастомного желания другом"
        test_ss_name = "test_decline_reserve_wish"

        # Authenticate and delete users before the test
        with allure.step("Аутентификация и удаление пользователей перед тестом"):
            auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend2)
        auth_controller.authenticate_and_register_user(TestData.phone_friend1, "Firsty", "11", "1111")
        auth_controller.authenticate_and_register_user(TestData.phone_friend2, "Vtoroy", "12", "1111")

        try:
            # Auth user 1
            with allure.step("Аутентификация первого пользователя"):
                main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)

            with allure.step("Переход к добавлению пользовательского подарка"):
                main_page_1.add_one_wish()

                main_page_1.click(TestData.BOTTOM_WISHES_BTN)
                time.sleep(2)
                main_page_1.click(MainPage.ADD_WISH_BUTTON)
                time.sleep(2)
                main_page_1.click(TestData.custom_wish_add_button)
                time.sleep(2)
                main_page_1.click(MainPage.ADD_CUSTOM_WISH_LINK)
                time.sleep(2)
                main_page_1.send_keys(MainPage.ADD_CUSTOM_WISH_LINK, TestData.parseWildberries)
                time.sleep(2)

            # Finalize custom gift addition
            with allure.step("Завершение добавления пользовательского подарка"):
                main_page_1.click(TestData.next_button)
                time.sleep(40)
                main_page_1.click(TestData.next_button)
                time.sleep(4)
                main_page_1.click(TestData.next_button)
                time.sleep(2)
                main_page_1.click(MainPage.DONE_BUTTON)
                time.sleep(3)
                main_page_1.click(TestData.BOTTOM_WISHES_BTN)
                time.sleep(3)

            # Проверяем вторым пользователем что подарок видно
            with allure.step("Проверка видимости подарка вторым пользователем"):
                main_page_1.logout(self)
                main_page_1.auth_by_phone(TestData.phone_friend2, TestData.confirm_code)

                main_page_1.is_element_visible(TestData.BOTTOM_FRIENDS_BTN_XP)
                main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
                time.sleep(2)
                main_page_1.is_element_visible(TestData.CONTACTS_FRIEND_1)
                main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
                time.sleep(4)


            # RESERVE WISH
            with allure.step("Резервирование желания"):
                time.sleep(2)
                main_page_1.swipe_up(600)
                time.sleep(2)
                main_page_1.click(TestData.FRIEND_WISH_KNIFES)
                time.sleep(2)
                main_page_1.scroll_until_visible(self.driver, MainPage.RESERVE_WISH_BUTTON)
                time.sleep(2)
                main_page_1.click(MainPage.RESERVE_WISH_BUTTON)
                time.sleep(2)
                main_page_1.click(MainPage.RESERVE_WISH_FINAL_BUTTON)
                time.sleep(2)



            # DECLINE WISH PHONE1
            with allure.step("Отклонение резервирования первым пользователем"):
                main_page_1.logout(self)
                main_page_1.auth_by_phone(TestData.phone_friend1, TestData.confirm_code)


                main_page_1.click(TestData.BOTTOM_WISHES_BTN)
                main_page_1.is_element_visible(TestData.FRIEND_WISH_KNIFES)
                main_page_1.click(TestData.FRIEND_WISH_KNIFES)

                main_page_1.scroll_until_visible(self.driver, MainPage.DECLINE_RESERVED_WISH)
                time.sleep(2)
                main_page_1.click(MainPage.DECLINE_RESERVED_WISH)
                time.sleep(2)
                main_page_1.click(MainPage.DECLINE_RESERVED_WISH_FINAL)
                time.sleep(2)

            with allure.step("Проверка отображения уведомления о доступности желания снова"):
                self.assertTrue(
                    main_page_1.is_element_visible(MainPage.NOTIFICATION_RESERVED_WISH_AVAILABLE_AGAIN),
                    "NOTIFICATION_WISH_SUGGESTED not visible!"
                )
                self.assertTrue(
                    main_page_1.is_element_invisible(MainPage.NOTIFICATION_RESERVED_WISH_AVAILABLE_AGAIN),
                    "NOTIFICATION_WISH_SUGGESTED not visible!"
                )

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



    @pytest.mark.reserve_wish_tests
    @pytest.mark.regress
    def test_reserve_custom_friend_gift_and_check_under_phone3(self):
        """Просмотр забронированного желания другим пользователем"""
        main_page_1 = MainPage(self.driver)

        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = "Просмотр забронированного желания другим пользователем"
        test_ss_name = "test_reserve_custom_friend_gift_and_check_under_phone3"

        # Authenticate and delete users before the test
        with allure.step("Аутентификация и удаление пользователей перед тестом"):
            auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
            auth_controller.authenticate_and_delete_user(TestData.phone_friend2)
            auth_controller.authenticate_and_delete_user(TestData.phone_friend3)
            auth_controller.authenticate_and_register_user(TestData.phone_friend1, TestData.friend1_name, "11", "1111")
            auth_controller.authenticate_and_register_user(TestData.phone_friend2, TestData.friend2_name, "12", "1111")
            auth_controller.authenticate_and_register_user(TestData.phone_friend3, TestData.friend3_name, "11", "1111")

        try:
            # Auth user 1
            with allure.step("Аутентификация первого пользователя"):
                main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)


            # Add custom gift
            with allure.step("Добавление пользовательского подарка"):

                main_page_1.add_one_wish()

                main_page_1.is_element_visible(TestData.BOTTOM_WISHES_BTN)
                main_page_1.click(TestData.BOTTOM_WISHES_BTN)
                time.sleep(2)
                main_page_1.is_element_visible(MainPage.ADD_WISH_BUTTON)
                main_page_1.click(MainPage.ADD_WISH_BUTTON)
                time.sleep(2)
                main_page_1.is_element_visible(TestData.custom_wish_add_button)
                main_page_1.click(TestData.custom_wish_add_button)
                time.sleep(2)
                main_page_1.click(MainPage.ADD_CUSTOM_WISH_LINK)
                time.sleep(2)
                main_page_1.send_keys(MainPage.ADD_CUSTOM_WISH_LINK, TestData.parseWildberries)
                time.sleep(2)
                main_page_1.click(TestData.next_button)
                time.sleep(40)
                main_page_1.click(TestData.next_button)
                time.sleep(4)
                main_page_1.click(TestData.next_button)
                time.sleep(2)
                main_page_1.click(MainPage.DONE_BUTTON)
                time.sleep(3)

            # Проверяем вторым пользователем что подарок видно
            with allure.step("Проверка видимости подарка вторым пользователем"):
                # Relogin
                main_page_1.logout(self.driver)
                main_page_1.auth_by_phone(TestData.phone_friend3, TestData.confirm_code)

                main_page_1.is_element_visible(TestData.BOTTOM_FRIENDS_BTN_XP)
                main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
                main_page_1.is_element_visible(TestData.CONTACTS_FRIEND_1)
                main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
                time.sleep(4)



            # RESERVE WISH
            with allure.step("Резервирование желания"):
                time.sleep(2)
                main_page_1.swipe_up(900)
                time.sleep(3)
                main_page_1.click_by_uiautomator_desc_contains("ножей")
                time.sleep(4)
                main_page_1.scroll_until_visible(self.driver, MainPage.RESERVE_WISH_BUTTON)
                time.sleep(2)
                main_page_1.click(MainPage.RESERVE_WISH_BUTTON)
                time.sleep(2)
                main_page_1.click(MainPage.RESERVE_WISH_FINAL_BUTTON)
                time.sleep(2)

            with allure.step("Проверка отображения уведомления о резервировании желания"):
                self.assertTrue(
                    main_page_1.is_element_visible(MainPage.NOTIFICATION_YOU_RESERVED_FRIEND_WISH),
                    "NOTIFICATION_WISH_SUGGESTED not visible!"
                )
                self.assertTrue(
                    main_page_1.is_element_invisible(MainPage.NOTIFICATION_YOU_RESERVED_FRIEND_WISH),
                    "NOTIFICATION_WISH_SUGGESTED not visible!"
                )

            # CHECK PHONE 3
            with allure.step("Проверка видимости подарка третьим пользователем"):
                main_page_1.logout(self.driver)
                time.sleep(2)
                main_page_1.auth_by_phone(TestData.phone_friend2, TestData.confirm_code)
                time.sleep(2)
                main_page_1.is_element_visible(TestData.BOTTOM_FRIENDS_BTN_XP)
                main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)


            with allure.step("Проверка видимости подарка третьим пользователем"):
                main_page_1.is_element_visible(TestData.CONTACTS_FRIEND_1)
                main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
                time.sleep(3)
                main_page_1.is_element_visible(TestData.FRIEND_WISH_KNIFES)


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

    @pytest.mark.reserve_wish_tests
    def test_accept_reserve_wish_then_add_it_to_self(self):
        """Добавление к себе заброннированное желание"""
        main_page_1 = MainPage(self.driver)

        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = ""
        test_ss_name = "test_accept_reserve_wish_then_add_it_to_self"

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

            self.assertTrue(main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                            "Profile settings button not visible!")
            self.assertTrue(main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                            "Profile settings button not visible!")

            # Navigate to add custom gift
            main_page_1.click(TestData.BOTTOM_WISHES_BTN)
            time.sleep(2)

            with allure.step("Нажатие кнопки добавления желания"):
                main_page_1.click(MainPage.ADD_WISH_BUTTON)
                time.sleep(2)

            with allure.step("Нажатие кнопки добавления кастомного желания"):
                main_page_1.click(TestData.custom_wish_add_button)
                time.sleep(2)

            with allure.step("Нажатие на ссылку для добавления кастомного желания"):
                main_page_1.click(MainPage.ADD_CUSTOM_WISH_LINK)
                time.sleep(2)

            with allure.step("Ввод ссылки для кастомного желания"):
                main_page_1.send_keys(MainPage.ADD_CUSTOM_WISH_LINK, TestData.parseWildberries)
                time.sleep(2)

            # Finalize custom gift addition
            with allure.step("Нажатие на кнопку 'Далее'"):
                main_page_1.click(TestData.next_button)

            time.sleep(40)

            with allure.step("Нажатие на кнопку 'Далее' снова"):
                main_page_1.click(TestData.next_button)
                time.sleep(4)

            with allure.step("Нажатие на кнопку 'Далее' еще раз"):
                main_page_1.click(TestData.next_button)
                time.sleep(2)

            with allure.step("Нажатие на кнопку 'Готово'"):
                main_page_1.click(MainPage.DONE_BUTTON)
                time.sleep(3)

            main_page_1.click(TestData.BOTTOM_WISHES_BTN)
            time.sleep(3)

            # Проверяем вторым пользователем что подарок видно
            # Relogin
            main_page_1.logout(self.driver)
            main_page_1.auth_by_phone(TestData.phone_friend2, TestData.confirm_code)

            main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
            time.sleep(2)
            main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
            time.sleep(4)

            # Screenshot block
            action_taken = "_privacy_all_check_by_second_phone"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)

            with allure.step("Снимок экрана с эталонным изображением видимости подарка"):
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
                allure.attach.file(ss_etalon, name="Etalon Screenshot", attachment_type=allure.attachment_type.PNG)

            with allure.step("Снимок экрана с результатом выполнения теста видимости подарка"):
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
                allure.attach.file(ss_run, name="Run Screenshot", attachment_type=allure.attachment_type.PNG)

            time.sleep(2)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # RESERVE WISH
            time.sleep(2)
            main_page_1.swipe_up(600)
            time.sleep(2)
            main_page_1.click(TestData.FRIEND_WISH_KNIFES)
            time.sleep(2)
            main_page_1.scroll_until_visible(self.driver, MainPage.RESERVE_WISH_BUTTON)
            time.sleep(2)

            with allure.step("Нажатие на кнопку 'Забронировать желание'"):
                main_page_1.click(MainPage.RESERVE_WISH_BUTTON)
                time.sleep(2)
                main_page_1.click(MainPage.RESERVE_WISH_FINAL_BUTTON)
                time.sleep(2)

            with allure.step("Проверка уведомления о резервировании желания"):
                self.assertTrue(
                    main_page_1.is_element_visible(MainPage.NOTIFICATION_YOU_RESERVED_FRIEND_WISH),
                    "NOTIFICATION_WISH_SUGGESTED not visible!"
                )
                self.assertTrue(
                    main_page_1.is_element_invisible(MainPage.NOTIFICATION_YOU_RESERVED_FRIEND_WISH),
                    "NOTIFICATION_WISH_SUGGESTED not visible!"
                )

            # ADD TO SELF
            time.sleep(2)
            main_page_1.click(MainPage.ADD_TO_SELF_OR_BUY_BUTTON)
            time.sleep(2)

            with allure.step("Нажатие на кнопку 'Добавить в себя'"):
                main_page_1.click(MainPage.ADD_WISH_WITHOUT_SETTINGS)
                time.sleep(2)

            with allure.step("Проверка уведомления о добавлении желания в себя"):
                self.assertTrue(
                    main_page_1.is_element_visible(MainPage.NOTIFICATION_WISH_ADDED),
                    "NOTIFICATION_WISH_SUGGESTED not visible!"
                )
                self.assertTrue(
                    main_page_1.is_element_invisible(MainPage.NOTIFICATION_WISH_ADDED),
                    "NOTIFICATION_WISH_SUGGESTED not visible!"
                )

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

    @pytest.mark.reserve_wish_tests
    def test_open_custom_gift_link_goldenapple(self):
        """Переход по ссылке в стороннем желании друга Золотое Яблоко"""
        main_page_1 = MainPage(self.driver)

        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = ""
        test_ss_name = "test_open_custom_gift_link_goldenapple"

        # Authenticate and delete users before the test
        with allure.step("Аутентификация и удаление пользователей перед тестом"):
            auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend2)
        auth_controller.authenticate_and_register_user(TestData.phone_friend1, "Firsty", "11", "1111")
        auth_controller.authenticate_and_register_user(TestData.phone_friend2, "Vtoroy", "12", "1111")

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
                time.sleep(2)

                main_page_1.click(TestData.custom_wish_add_button)
                time.sleep(2)

                main_page_1.click(MainPage.ADD_CUSTOM_WISH_LINK)
                time.sleep(2)

                main_page_1.send_keys(MainPage.ADD_CUSTOM_WISH_LINK, TestData.parseGoldapple)
                time.sleep(2)

            # Finalize custom gift addition
            with allure.step("Завершение добавления пользовательского подарка"):
                main_page_1.click(TestData.next_button)
                time.sleep(40)

                main_page_1.click(TestData.next_button)
                time.sleep(4)

                main_page_1.click(TestData.next_button)
                time.sleep(2)

                main_page_1.click(MainPage.DONE_BUTTON)
                time.sleep(3)

            # Проверяем вторым пользователем что подарок видно
            with allure.step("Проверка видимости подарка вторым пользователем"):
                main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
                time.sleep(2)
                main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
                time.sleep(4)

            # Screenshot block
            with allure.step("Снимок экрана с эталонным изображением видимости подарка"):
                action_taken = "_privacy_all_check_by_second_phone"
                ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
                ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
                allure.attach.file(ss_etalon, name="Etalon Screenshot", attachment_type=allure.attachment_type.PNG)
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
                allure.attach.file(ss_run, name="Run Screenshot", attachment_type=allure.attachment_type.PNG)
                time.sleep(2)
                assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # CUSTOM WISH OPEN LINK
            with allure.step("Открытие ссылки на стороннее желание"):
                main_page_1.click(TestData.FRIEND_WISH_KNIFES)
                time.sleep(4)
                main_page_1.click(MainPage.OPEN_CUSTOM_WISH_LINK)
                time.sleep(15)

            # Screenshot block
            with allure.step("Снимок экрана после открытия ссылки на стороннее желание"):
                action_taken = "_OPEN_CUSTOM_WISH_LINK"
                ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
                ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
                allure.attach.file(ss_etalon, name="Etalon Screenshot", attachment_type=allure.attachment_type.PNG)
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
                allure.attach.file(ss_run, name="Run Screenshot", attachment_type=allure.attachment_type.PNG)
                time.sleep(2)
                assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            with allure.step("Закрытие веб-вью"):
                main_page_1.click(MainPage.CLOSE_WEBVIEW)
                time.sleep(4)

            # Screenshot block
            with allure.step("Снимок экрана после закрытия веб-вью"):
                action_taken = "_CLOSE_WEBVIEW"
                ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
                ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
                allure.attach.file(ss_etalon, name="Etalon Screenshot", attachment_type=allure.attachment_type.PNG)
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
                allure.attach.file(ss_run, name="Run Screenshot", attachment_type=allure.attachment_type.PNG)
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

    @pytest.mark.reserve_wish_tests
    @allure.story("Тест: Переход по ссылке в стороннем желании друга OZON")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_open_custom_gift_link_ozon(self):
        """Переход по ссылке в стороннем желании друга OZON"""
        main_page_1 = MainPage(self.driver)

        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = ""
        test_ss_name = "test_open_custom_gift_link_ozon"

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

            self.assertTrue(main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                            "Profile settings button not visible!")
            self.assertTrue(main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                            "Profile settings button not visible!")

            # Navigate to add custom gift
            with allure.step("Нажатие кнопки нижнего меню 'Желания'"):
                main_page_1.click(TestData.BOTTOM_WISHES_BTN)
                time.sleep(2)

            with allure.step("Нажатие кнопки 'Добавить желание'"):
                main_page_1.click(MainPage.ADD_WISH_BUTTON)
                time.sleep(2)

            with allure.step("Нажатие кнопки 'Добавить кастомное желание'"):
                main_page_1.click(TestData.custom_wish_add_button)
                time.sleep(2)

            with allure.step("Нажатие кнопки 'Добавить ссылку кастомного желания'"):
                main_page_1.click(MainPage.ADD_CUSTOM_WISH_LINK)
                time.sleep(2)

            with allure.step("Ввод ссылки кастомного желания OZON"):
                main_page_1.send_keys(MainPage.ADD_CUSTOM_WISH_LINK, TestData.parseOzon)
                time.sleep(2)

            # Finalize custom gift addition
            with allure.step("Подтверждение добавления кастомного подарка"):
                main_page_1.click(TestData.next_button)
                time.sleep(40)

                main_page_1.click(TestData.next_button)
                time.sleep(4)

                main_page_1.click(TestData.next_button)
                time.sleep(2)

                main_page_1.click(MainPage.DONE_BUTTON)
                time.sleep(3)

            # Проверка второго пользователя
            with allure.step("Проверка видимости подарка у второго пользователя"):
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

                with allure.step("Снимок экрана с результатом проверки видимости подарка"):
                    allure.attach.file(ss_run, name="Run Screenshot", attachment_type=allure.attachment_type.PNG)

            # CUSTOM WISH OPEN LINK
            with allure.step("Открытие кастомной ссылки желания"):
                main_page_1.click(TestData.FRIEND_WISH_KNIFES)
                time.sleep(4)
                main_page_1.click(MainPage.OPEN_CUSTOM_WISH_LINK)
                time.sleep(15)

                # Screenshot block
                action_taken = "_OPEN_CUSTOM_WISH_LINK"
                ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
                ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
                time.sleep(2)
                assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

                with allure.step("Снимок экрана с результатом открытия кастомной ссылки"):
                    allure.attach.file(ss_run, name="Run Screenshot", attachment_type=allure.attachment_type.PNG)

            # Закрытие WebView
            with allure.step("Закрытие WebView"):
                main_page_1.click(MainPage.CLOSE_WEBVIEW)
                time.sleep(4)

                # Screenshot block
                action_taken = "_CLOSE_WEBVIEW"
                ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
                ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
                time.sleep(2)
                assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

                with allure.step("Снимок экрана с результатом закрытия WebView"):
                    allure.attach.file(ss_run, name="Run Screenshot", attachment_type=allure.attachment_type.PNG)

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

    @pytest.mark.reserve_wish_tests
    @allure.story("Переход по ссылке в стороннем желании друга MEGA")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_open_custom_gift_link_mega(self):
        """Переход по ссылке в стороннем желании друга MEGA"""
        main_page_1 = MainPage(self.driver)

        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = ""
        test_ss_name = "test_open_custom_gift_link_mega"

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

            self.assertTrue(main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                            "Profile settings button not visible!")
            self.assertTrue(main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                            "Profile settings button not visible!")

            # Navigate to add custom gift
            with allure.step("Нажатие кнопки нижнего меню желаемого"):
                main_page_1.click(TestData.BOTTOM_WISHES_BTN)
                time.sleep(2)

            with allure.step("Нажатие кнопки добавления желания"):
                main_page_1.click(MainPage.ADD_WISH_BUTTON)
                time.sleep(2)

            with allure.step("Нажатие кнопки добавления кастомного желания"):
                main_page_1.click(TestData.custom_wish_add_button)
                time.sleep(2)

            with allure.step("Нажатие кнопки добавления ссылки на кастомное желание"):
                main_page_1.click(MainPage.ADD_CUSTOM_WISH_LINK)
                time.sleep(2)

            with allure.step("Отправка ссылки на кастомное желание"):
                main_page_1.send_keys(MainPage.ADD_CUSTOM_WISH_LINK, TestData.parseMegamarket)
                time.sleep(2)

            # Finalize custom gift addition
            with allure.step("Нажатие кнопки 'Далее'"):
                main_page_1.click(TestData.next_button)

            time.sleep(40)

            with allure.step("Подтверждение действия с кастомным желанием"):
                main_page_1.click(TestData.next_button)
                time.sleep(4)

                main_page_1.click(TestData.next_button)
                time.sleep(2)

                main_page_1.click(MainPage.DONE_BUTTON)
                time.sleep(3)

            # Проверяем вторым пользователем что подарок видно
            with allure.step("Проверка видимости подарка у второго пользователя"):
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
                allure.attach.file(ss_etalon, name="Etalon Screenshot", attachment_type=allure.attachment_type.PNG)
                allure.attach.file(ss_run, name="Run Screenshot", attachment_type=allure.attachment_type.PNG)
                assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # CUSTOM WISH OPEN LINK
            with allure.step("Открытие кастомного желания с ссылкой"):
                main_page_1.click(TestData.FRIEND_WISH_KNIFES)
                time.sleep(4)
                main_page_1.click(MainPage.OPEN_CUSTOM_WISH_LINK)
                time.sleep(15)

                # Screenshot block
                action_taken = "_OPEN_CUSTOM_WISH_LINK"
                ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
                ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
                time.sleep(2)
                allure.attach.file(ss_etalon, name="Etalon Screenshot", attachment_type=allure.attachment_type.PNG)
                allure.attach.file(ss_run, name="Run Screenshot", attachment_type=allure.attachment_type.PNG)
                assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            with allure.step("Закрытие веб-страницы"):
                main_page_1.click(MainPage.CLOSE_WEBVIEW)
                time.sleep(4)

                # Screenshot block
                action_taken = "_CLOSE_WEBVIEW"
                ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
                ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
                time.sleep(2)
                allure.attach.file(ss_etalon, name="Etalon Screenshot", attachment_type=allure.attachment_type.PNG)
                allure.attach.file(ss_run, name="Run Screenshot", attachment_type=allure.attachment_type.PNG)
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

    @pytest.mark.reserve_wish_tests
    @allure.story("Переход по ссылке в стороннем желании друга Lamoda")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_open_custom_gift_link_lamoda(self):
        """Переход по ссылке в стороннем желании друга Lamoda"""
        main_page_1 = MainPage(self.driver)

        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = ""
        test_ss_name = "test_open_custom_gift_link_lamoda"

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

            self.assertTrue(main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                            "Profile settings button not visible!")
            self.assertTrue(main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                            "Profile settings button not visible!")

            # Навигация к добавлению кастомного подарка
            with allure.step("Переход к добавлению кастомного подарка"):
                main_page_1.click(TestData.BOTTOM_WISHES_BTN)
                time.sleep(2)
                main_page_1.click(MainPage.ADD_WISH_BUTTON)
                time.sleep(2)

                main_page_1.click(TestData.custom_wish_add_button)
                time.sleep(2)

                main_page_1.click(MainPage.ADD_CUSTOM_WISH_LINK)
                time.sleep(2)

                main_page_1.send_keys(MainPage.ADD_CUSTOM_WISH_LINK, TestData.parseLamoda)
                time.sleep(2)

            # Завершение добавления кастомного подарка
            with allure.step("Завершение добавления кастомного подарка"):
                main_page_1.click(TestData.next_button)
                time.sleep(40)

                main_page_1.click(TestData.next_button)
                time.sleep(4)

                main_page_1.click(TestData.next_button)
                time.sleep(2)

                main_page_1.click(MainPage.DONE_BUTTON)
                time.sleep(3)

            # Проверка видимости подарка вторым пользователем
            with allure.step("Проверка видимости подарка вторым пользователем"):
                main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
                time.sleep(2)
                main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
                time.sleep(4)

                # Screenshot block
                action_taken = "_privacy_all_check_by_second_phone"
                ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
                ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
                allure.attach.file(ss_etalon, name="Etalon Screenshot", attachment_type=allure.attachment_type.PNG)
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
                allure.attach.file(ss_run, name="Run Screenshot", attachment_type=allure.attachment_type.PNG)
                time.sleep(2)
                assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Открытие кастомного подарка по ссылке
            with allure.step("Открытие кастомного подарка по ссылке"):
                main_page_1.click(TestData.FRIEND_WISH_KNIFES)
                time.sleep(4)
                main_page_1.click(MainPage.OPEN_CUSTOM_WISH_LINK)
                time.sleep(15)

                # Screenshot block
                action_taken = "_OPEN_CUSTOM_WISH_LINK"
                ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
                ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
                allure.attach.file(ss_etalon, name="Etalon Screenshot", attachment_type=allure.attachment_type.PNG)
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
                allure.attach.file(ss_run, name="Run Screenshot", attachment_type=allure.attachment_type.PNG)
                time.sleep(2)
                assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Закрытие вебвью
            with allure.step("Закрытие вебвью"):
                main_page_1.click(MainPage.CLOSE_WEBVIEW)
                time.sleep(4)

                # Screenshot block
                action_taken = "_CLOSE_WEBVIEW"
                ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
                ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
                allure.attach.file(ss_etalon, name="Etalon Screenshot", attachment_type=allure.attachment_type.PNG)
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
                allure.attach.file(ss_run, name="Run Screenshot", attachment_type=allure.attachment_type.PNG)
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

    @pytest.mark.reserve_wish_tests
    @allure.story("Переход по ссылке в стороннем желании друга WILD")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_open_custom_gift_link_wild(self):
        """Переход по ссылке в стороннем желании друга WILD"""
        main_page_1 = MainPage(self.driver)

        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = ""
        test_ss_name = "test_open_custom_gift_link_wild"

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

            self.assertTrue(main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                            "Profile settings button not visible!")
            self.assertTrue(main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
                            "Profile settings button not visible!")

            # Navigate to add custom gift
            with allure.step("Нажатие кнопки добавления желания"):
                main_page_1.click(TestData.BOTTOM_WISHES_BTN)
                time.sleep(2)
                allure.attach("Нажата кнопка добавления желания", name="Step Description",
                              attachment_type=allure.attachment_type.TEXT)

            with allure.step("Выбор кнопки добавления нового желания"):
                main_page_1.click(MainPage.ADD_WISH_BUTTON)
                time.sleep(2)

            with allure.step("Выбор кнопки добавления кастомного желания"):
                main_page_1.click(TestData.custom_wish_add_button)
                time.sleep(2)

            with allure.step("Нажатие кнопки добавления кастомной ссылки желания"):
                main_page_1.click(MainPage.ADD_CUSTOM_WISH_LINK)
                time.sleep(2)

            with allure.step("Отправка ссылки на кастомное желание"):
                main_page_1.send_keys(MainPage.ADD_CUSTOM_WISH_LINK, TestData.parseWildberries)
                time.sleep(2)

            # Finalize custom gift addition
            with allure.step("Подтверждение добавления кастомного желания"):
                main_page_1.click(TestData.next_button)
                time.sleep(40)

                main_page_1.click(TestData.next_button)
                time.sleep(4)

                main_page_1.click(TestData.next_button)
                time.sleep(2)

                main_page_1.click(MainPage.DONE_BUTTON)
                time.sleep(3)

            # Проверяем вторым пользователем что подарок видно
            with allure.step("Проверка доступности подарка вторым пользователем"):
                main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
                time.sleep(2)
                main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
                time.sleep(4)

                # Screenshot block
                action_taken = "_privacy_all_check_by_second_phone"
                ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
                ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
                allure.attach.file(ss_etalon, name="Etalon Screenshot", attachment_type=allure.attachment_type.PNG)
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
                allure.attach.file(ss_run, name="Run Screenshot", attachment_type=allure.attachment_type.PNG)
                time.sleep(2)
                assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # CUSTOM WISH OPEN LINK
            with allure.step("Открытие кастомной ссылки желания"):
                main_page_1.click(TestData.FRIEND_WISH_KNIFES)
                time.sleep(4)
                main_page_1.click(MainPage.OPEN_CUSTOM_WISH_LINK)
                time.sleep(15)

                # Screenshot block
                action_taken = "_OPEN_CUSTOM_WISH_LINK"
                ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
                ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
                allure.attach.file(ss_etalon, name="Etalon Screenshot", attachment_type=allure.attachment_type.PNG)
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
                allure.attach.file(ss_run, name="Run Screenshot", attachment_type=allure.attachment_type.PNG)
                time.sleep(2)
                assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            with allure.step("Закрытие WebView"):
                main_page_1.click(MainPage.CLOSE_WEBVIEW)
                time.sleep(4)

                # Screenshot block
                action_taken = "_CLOSE_WEBVIEW"
                ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
                ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
                allure.attach.file(ss_etalon, name="Etalon Screenshot", attachment_type=allure.attachment_type.PNG)
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
                allure.attach.file(ss_run, name="Run Screenshot", attachment_type=allure.attachment_type.PNG)
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
