import logging
import re
import time
import traceback

import allure
import pytest

from ResultCollector import ResultCollector
from core.pages import main_page
from core.pages.main_page import MainPage
from core.data.test_data import TestData
from reporting.TelegramReport import TelegramReport
from core.pages.base_test import BaseTest
from core.api.AuthController import AuthController


class Contacts(BaseTest):

    @pytest.mark.regress
    @pytest.mark.contacts_tests
    def test_create_friend_contact_system_app_closing(self):
        """Сценарий добавления друга через системный UI (GB закрывается и открывается после добавления)"""
        status = "🟡"
        bug_link = "/-/issues/3353"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = "Контакты: Добавление друга через системный UI (GB закрывается и открывается после добавления)"
        test_ss_name = "test_create_friend_contact_system_app_closing"
        main_page_1 = MainPage(self.driver)

        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        # Authenticate and delete users before the test
        auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend2)
        #auth_controller.authenticate_and_register_user(TestData.phone_friend1, "Firsty", "11", "1111")
        #auth_controller.authenticate_and_register_user(TestData.phone_friend2, "Vtoroy", "12", "1111")

        try:
            # Auth
            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend2, TestData.confirm_code)
            main_page_1.register_new_user(self.driver, TestData.phone_friend2)

            main_page_1.logout(self)

            main_page_1.auth_by_phone(TestData.phone_friend1, TestData.confirm_code)
            main_page_1.register_new_user(self.driver, TestData.phone_friend1)

            main_page_1.is_element_visible(TestData.BOTTOM_FRIENDS_BTN_XP)
            main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
            main_page_1.is_element_invisible(TestData.CONTACTS_FRIEND_1)

            main_page_1.is_element_visible(TestData.BOTTOM_HOME_BTN_XP)
            main_page_1.click(TestData.BOTTOM_HOME_BTN_XP)
            time.sleep(1)
            main_page_1.exit_app()
            main_page_1.open_add_contact_screen()
            time.sleep(5)

            main_page_1.open_GB_app()
            #main_page_1.auth_by_phone(TestData.phone_friend1, TestData.confirm_code)

            main_page_1.is_element_visible(TestData.BOTTOM_FRIENDS_BTN_XP)
            main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)

            main_page_1.is_element_visible(TestData.CONTACTS_FRIEND_1)


            status = "🟢"
        except Exception as e:
            status = "🟡"
            duration = time.time() - start_time
            collector.add_result(test_name_this, status, report_url, duration, bug_link)
            raise e
        finally:
            duration = time.time() - start_time
            collector.add_result(test_name_this, status, report_url, duration, bug_link)

    @pytest.mark.regress
    @pytest.mark.contacts_tests
    def test_create_friend_contact_system_app_hiding(self):
        """Сценарий добавления друга через системный UI (GB сворачивается и возвращается после добавления)"""
        status = "🟡"
        bug_link = "/-/issues/3353"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = "Контакты: Добавление друга через системный UI (GB сворачивается и возвращается после добавления)"
        test_ss_name = "test_create_friend_contact_system_app_hiding"
        main_page_1 = MainPage(self.driver)

        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        # Authenticate and delete users before the test
        auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend2)
        # auth_controller.authenticate_and_register_user(TestData.phone_friend1, "Firsty", "11", "1111")
        #auth_controller.authenticate_and_register_user(TestData.phone_friend2, "Vtoroy", "12", "1111")

        try:
            # Auth
            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend2, TestData.confirm_code)
            main_page_1.register_new_user(self.driver, TestData.phone_friend2)

            main_page_1.logout(self)

            main_page_1.auth_by_phone(TestData.phone_friend1, TestData.confirm_code)
            main_page_1.register_new_user(self.driver, TestData.phone_friend1)

            main_page_1.is_element_visible(TestData.BOTTOM_FRIENDS_BTN_XP)
            main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
            main_page_1.is_element_invisible(TestData.CONTACTS_FRIEND_1)
            time.sleep(2)
            self.driver.press_keycode(3)  # HOME
            time.sleep(1)
            main_page_1.open_add_contact_screen()
            time.sleep(5)

            main_page_1.open_GB_app()
            # main_page_1.auth_by_phone(TestData.phone_friend1, TestData.confirm_code)
            time.sleep(8)
            main_page_1.is_element_visible(TestData.BOTTOM_FRIENDS_BTN_XP)
            main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
            main_page_1.is_element_visible(TestData.CONTACTS_FRIEND_1)

            status = "🟢"
        except Exception as e:
            status = "🟡"
            duration = time.time() - start_time
            collector.add_result(test_name_this, status, report_url, duration, bug_link)
            raise e
        finally:
            duration = time.time() - start_time
            collector.add_result(test_name_this, status, report_url, duration, bug_link)


    @pytest.mark.regress
    @pytest.mark.contacts_tests
    def test_create_friend_ptr(self):
        """Сценарий добавления друга (PTR)"""
        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = "Контакты: Добавление друга, PTR"
        test_ss_name = "test_create_friend_ptr"
        main_page_1 = MainPage(self.driver)

        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        # Authenticate and delete users before the test
        auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend2)


        try:
            # Auth
            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend2, TestData.confirm_code)
            main_page_1.register_new_user(self.driver, TestData.phone_friend2)

            main_page_1.logout(self)

            main_page_1.auth_by_phone(TestData.phone_friend1, TestData.confirm_code)
            main_page_1.register_new_user(self.driver, TestData.phone_friend1)

            main_page_1.is_element_visible(TestData.BOTTOM_FRIENDS_BTN_XP)
            main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)

            main_page_1.is_element_invisible(TestData.CONTACTS_FRIEND_1)
            time.sleep(2)

            auth_controller.authenticate_and_register_user(TestData.phone_friend1, "Firsty", "11", "1111")
            auth_controller.authenticate_and_register_user(TestData.phone_friend2, "Vtoroy", "12", "1111")

            main_page_1.swipe_down(800)
            time.sleep(2)

            main_page_1.is_element_visible(TestData.BOTTOM_FRIENDS_BTN_XP)
            main_page_1.is_element_visible(TestData.CONTACTS_FRIEND_1)

            status = "🟢"
        except Exception as e:
            status = "🔴"
            duration = time.time() - start_time
            collector.add_result(test_name_this, status, report_url, duration)
            raise e
        finally:
            duration = time.time() - start_time
            collector.add_result(test_name_this, status, report_url, duration)

    @pytest.mark.regress
    @pytest.mark.contacts_tests
    def test_create_group_with_picture(self):
        """Создание группы с обложкой"""
        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = "Контакты: Создание группы с обложкой"
        test_ss_name = "test_create_group_with_picture"
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

            # contacts
            main_page_1.is_element_visible(TestData.BOTTOM_FRIENDS_BTN_XP)
            main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)

            # Navigate to contacts
            with allure.step("Навигация к списку контактов"):
                main_page_1.is_element_visible(TestData.contacts_my_groups_button)
                main_page_1.click(TestData.contacts_my_groups_button)

            # create group
            with allure.step("Создание группы"):
                main_page_1.is_element_visible(MainPage.MY_GROUPS_NO_GROUPS_TEXT)
                main_page_1.is_element_visible(TestData.create_group_button)
                main_page_1.click(TestData.create_group_button)

                main_page_1.is_element_visible(TestData.create_group_text_field)
                main_page_1.click(TestData.create_group_text_field)
                main_page_1.send_keys_simple("Test")

            # Finalize group creation
            with allure.step("Завершение создания группы"):
                main_page_1.click(TestData.next_button)

                main_page_1.is_element_visible(TestData.CREATE_GROUP_ADD_FRIEND_0)
                main_page_1.click_by_uiautomator(TestData.CREATE_GROUP_ADD_FRIEND_0)
                main_page_1.click(MainPage.DONE_BUTTON)

                main_page_1.is_element_visible(TestData.CREATE_GROUP_SELECT_COVER_PICTURE_1)
                main_page_1.click_by_uiautomator(TestData.CREATE_GROUP_SELECT_COVER_PICTURE_1)

                main_page_1.click(MainPage.DONE_BUTTON)

            self.assertTrue(
                main_page_1.is_element_visible(MainPage.NOTIFICATION_GROUP_CREATED),
                "NOTIFICATION_GROUP_CREATED not visible!"
            )
            self.assertTrue(
                main_page_1.is_element_invisible(MainPage.NOTIFICATION_GROUP_CREATED),
                "NOTIFICATION_GROUP_CREATED not visible!"
            )



            # Проверка видимости группы из контактов
            with allure.step("Проверка видимости группы из списка контактов"):

                main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)

                main_page_1.is_element_visible(TestData.contacts_my_groups_button)
                main_page_1.click(TestData.contacts_my_groups_button)



            # edit group
            with allure.step("Редактирование группы"):
                time.sleep(2)
                main_page_1.click_by_uiautomator(TestData.my_groups_first_group)
                main_page_1.is_element_visible(TestData.MY_GROUPS_OPENED_GROUP_EDIT_BUTTON)
                main_page_1.click_by_uiautomator(TestData.MY_GROUPS_OPENED_GROUP_EDIT_BUTTON)
                main_page_1.is_element_visible(TestData.MY_GROUPS_EDIT_GROUP_NAME_FIELD)
                main_page_1.click_by_uiautomator(TestData.MY_GROUPS_EDIT_GROUP_NAME_FIELD)
                main_page_1.send_keys_simple("1234")
                main_page_1.click(MainPage.DONE_BUTTON)
                time.sleep(3)



            # update group
            with allure.step("Add new ppl to group"):
                time.sleep(2)
                main_page_1.click_by_uiautomator(TestData.ADD_BUTTON)
                main_page_1.is_element_visible(TestData.CREATE_GROUP_ADD_FRIEND_1)
                main_page_1.click_by_uiautomator(TestData.CREATE_GROUP_ADD_FRIEND_1)
                time.sleep(1)
                main_page_1.click(MainPage.DONE_BUTTON)



            # удаление группы
            with allure.step("Удаление группы"):
                time.sleep(2)
                main_page_1.click_by_uiautomator(TestData.opened_group_edit_button)
                main_page_1.is_element_visible(TestData.edit_group_delete_group)
                main_page_1.click(TestData.edit_group_delete_group)
                main_page_1.is_element_visible(TestData.edit_group_delete_group_confirm)
                main_page_1.click(TestData.edit_group_delete_group_confirm)

                main_page_1.is_element_visible(TestData.BOTTOM_HOME_BTN_XP)
                main_page_1.click(TestData.BOTTOM_HOME_BTN_XP)

            status = "🟢"
        except Exception as e:
            status = "🔴"
            duration = time.time() - start_time
            collector.add_result(test_name_this, status, report_url, duration)
            raise e
        finally:
            duration = time.time() - start_time
            collector.add_result(test_name_this, status, report_url, duration)

    @pytest.mark.regress
    @pytest.mark.contacts_tests
    def test_create_group_without_picture(self):
        """Создание группы БЕЗ обложки"""
        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = "Контакты: Создание группы БЕЗ обложки"
        test_ss_name = "test_create_group_without_picture"
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
            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)

            # Navigate to contacts
            with allure.step("Переход в контакты"):
                main_page_1.is_element_visible(TestData.BOTTOM_FRIENDS_BTN_XP)
                main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
                # TelegramReport.send_tg("click(MainPage.GIFT_LIST_LOCATOR)")
                time.sleep(2)

            with allure.step("Переход в мои группы"):
                main_page_1.is_element_visible(TestData.contacts_my_groups_button)
                main_page_1.click(TestData.contacts_my_groups_button)
                # TelegramReport.send_tg("click(MainPage.contacts_my_groups)")
                time.sleep(2)

            self.assertTrue(
                main_page_1.is_element_visible(MainPage.MY_GROUPS_NO_GROUPS_TEXT),
                "Profile settings button not visible!"
            )
            # TelegramReport.send_tg("MY_GROUPS_NO_GROUPS_TEXT visible")

            # Create group
            with allure.step("Создание группы"):
                main_page_1.is_element_visible(TestData.create_group_button)
                main_page_1.click(TestData.create_group_button)
                # TelegramReport.send_tg("click(.create_group_button)")
                time.sleep(2)

            with allure.step("Ввод названия группы"):
                main_page_1.is_element_visible(TestData.create_group_text_field)
                main_page_1.click(TestData.create_group_text_field)
                # TelegramReport.send_tg("click(.create_group_text_field)")
                time.sleep(2)

                main_page_1.send_keys_simple("Group Test Name")
                main_page_1.is_element_visible(TestData.next_button)
                main_page_1.click(TestData.next_button)
            time.sleep(2)

            # Add first friend
            with allure.step("Добавление первого друга"):
                main_page_1.is_element_visible(TestData.create_group_add_first_friend)
                main_page_1.click_by_uiautomator(TestData.create_group_add_first_friend)
                # TelegramReport.send_tg("click(MainPage.NEXT_BUTTON)")

            with allure.step("Подтверждение создания группы"):
                main_page_1.is_element_visible(MainPage.DONE_BUTTON)
                main_page_1.click(MainPage.DONE_BUTTON)
                # TelegramReport.send_tg("click(MainPage.DONE_BUTTON)")
                time.sleep(2)
                main_page_1.click(MainPage.DONE_BUTTON)
            # TelegramReport.send_tg("click(MainPage.DONE_BUTTON)")

            time.sleep(5)
            with allure.step("Проверка видимости группы, ее названия и количества человек"):
                main_page_1.is_element_visible(TestData.my_groups_first_group)
                main_page_1.click_by_uiautomator(TestData.my_groups_first_group)

                main_page_1.is_element_visible(TestData.CONTACT_GROUP_PPL_COUNT)

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
    @pytest.mark.contacts_tests
    def test_register_with_bday_soon(self):

        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_ss_name = "test_register_with_bday_soon"
        test_name_this = "Контакты: Регистрация когда скоро день рождения"
        main_page_1 = MainPage(self.driver)
        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        # Authenticate and delete users before the test
        auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend2)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend3)
        auth_controller.authenticate_and_register_user(TestData.phone_friend1, "Firsty", "20", "1111")
        auth_controller.authenticate_and_register_user(TestData.phone_friend2, "Vtoroy", "11", "1111")
        auth_controller.authenticate_and_register_user(TestData.phone_friend3, "Treti", "121", "1111")

        try:
            # logout 2
            time.sleep(2)
            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend3, TestData.confirm_code)
            time.sleep(2)
            main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
            time.sleep(3)
            main_page_1.swipe_down(1999)
            time.sleep(2)

            # Проверка Отображается список друзей с приближающимися днями рожденьями в рамках 30 дней в хронологическом порядке
            main_page_1.is_element_visible(TestData.DBAY_WIDGET)
            #TODO чтобы корректно проверять в хронологическом порядке нужна доработка на фронте


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
    @pytest.mark.contacts_tests
    def test_bday_widget_not_visible(self):
        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_ss_name = "test_bday_widget_not_visible"
        test_name_this = "Контакты: Виджет День Рождения не отображается"
        main_page_1 = MainPage(self.driver)
        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        # Authenticate and delete users before the test
        auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend2)
        auth_controller.authenticate_and_register_user(TestData.phone_friend1, "Firsty", "111", "1111")
        auth_controller.authenticate_and_register_user(TestData.phone_friend2, "Vtoroy", "123", "1111")

        try:
            # Auth
            time.sleep(20)
            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend2, TestData.confirm_code)

            # refresh contacts
            time.sleep(2)
            main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
            time.sleep(2)
            main_page_1.swipe_down(1999)
            time.sleep(3)

            main_page_1.is_element_invisible(TestData.DBAY_WIDGET)

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
    @pytest.mark.contacts_tests
    def test_friend_toggles(self):
        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_ss_name = "test_friend_toggles"
        test_name_this = "Контакты: Выставляем избранность контакта, Выключить уведомления у друга и Скрыть из ленты"
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
        auth_controller.authenticate_and_register_user(TestData.phone_friend3, "Treti", "12", "1111")

        try:
            # Auth
            time.sleep(20)
            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)

            # refresh contacts
            time.sleep(2)
            main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
            time.sleep(2)
            main_page_1.swipe_down(1999)
            time.sleep(2)
            main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
            time.sleep(2)
            main_page_1.click(TestData.CONTACTS_OPENED_FRIEND_ADD_TO_FAVORITE2)
            time.sleep(2)

            # TODO чтобы корректно проверять видимость избранного нужна доработка на фронте

            main_page_1.click(TestData.CONTACTS_OPENED_FRIEND_ADD_TO_FAVORITE2)
            time.sleep(2)

            # TODO чтобы корректно проверять видимость избранного нужна доработка на фронте

            time.sleep(2)
            main_page_1.click(TestData.CONTACTS_OPENED_FRIEND_SETTINGS)
            time.sleep(2)
            main_page_1.click(TestData.CONTACTS_OPENED_FRIEND_SETTINGS_NOTIF_OFF)
            time.sleep(2)

            # TODO чтобы корректно проверять видимость уведомлений нужна доработка на фронте

            time.sleep(2)
            main_page_1.click(TestData.CONTACTS_OPENED_FRIEND_SETTINGS)
            time.sleep(2)
            main_page_1.click(TestData.CONTACTS_OPENED_FRIEND_SETTINGS_NOTIF_ON)
            time.sleep(2)

            # TODO чтобы корректно проверять видимость уведомлений нужна доработка на фронте

            time.sleep(2)
            main_page_1.click(TestData.CONTACTS_OPENED_FRIEND_SETTINGS)
            time.sleep(2)
            main_page_1.click(TestData.CONTACTS_OPENED_FRIEND_SETTINGS_FEED_ON)

            # TODO чтобы корректно проверять видимость в ленте нужна доработка на фронте

            time.sleep(2)
            main_page_1.click(TestData.CONTACTS_OPENED_FRIEND_SETTINGS)
            time.sleep(2)
            main_page_1.click(TestData.CONTACTS_OPENED_FRIEND_SETTINGS_FEED_OFF)

            # TODO чтобы корректно проверять видимость в ленте нужна доработка на фронте

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
