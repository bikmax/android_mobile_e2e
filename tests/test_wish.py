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


class Wish(BaseTest):

    @pytest.mark.regress
    @pytest.mark.wish_tests
    def test_ai_wish_open(self):
        """BUG: ждем ID /-/issues/2287"""
        test_name_this = "Открытие желания через рекомендацию AI"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        #status = "🔴"
        status = "🟡"
        bug_link = "/-/issues/2287"
        collector = ResultCollector()
        main_page = MainPage(self.driver)
        auth = AuthController()
        start_time = time.time()  # Фиксируем время начала теста

        try:
            # Подготовка и выполнение теста
            auth.authenticate_and_delete_user(TestData.phone_friend1)
            auth.authenticate_and_register_user(TestData.phone_friend1, TestData.friend1_name, "11", "1111")
            main_page.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)
            time.sleep(2)
            main_page.is_element_visible(TestData.BOTTOM_AI_BTN_XP)
            main_page.click(TestData.BOTTOM_AI_BTN_XP)
            time.sleep(2)
            main_page.is_element_visible(TestData.AI_SEARCH_FIELD)
            main_page.click(TestData.AI_SEARCH_FIELD)
            main_page.send_keys_simple("fisherman")

            main_page.is_element_visible(TestData.AI_SEND_MESSAGE)
            main_page.click(TestData.AI_SEND_MESSAGE)

            main_page.is_element_visible(TestData.AI_SEARCH_FIELD)
            main_page.click(TestData.AI_SEARCH_FIELD)
            main_page.send_keys_simple("3000")

            main_page.is_element_visible(TestData.AI_SEND_MESSAGE)
            main_page.click(TestData.AI_SEND_MESSAGE)
            time.sleep(5)

            main_page.is_element_visible(TestData.AI_RESULT_1)
            main_page.click(TestData.AI_RESULT_1)

            main_page.is_element_visible(MainPage.ADD_TO_WISHES_OR_BUY_BUTTON)
            main_page.click(MainPage.ADD_TO_WISHES_OR_BUY_BUTTON)

            main_page.is_element_visible(MainPage.ADD_WISH_WITHOUT_SETTINGS)
            main_page.click(MainPage.ADD_WISH_WITHOUT_SETTINGS)

            main_page.is_element_visible(TestData.BOTTOM_WISHES_BTN)
            main_page.click(TestData.BOTTOM_WISHES_BTN)

            main_page.is_element_visible(TestData.MY_WISHES_FIRST_WISH)


            status = "🟢"
        except Exception as e:
            #status = "🔴"
            status = "🟡"
            duration = time.time() - start_time
            collector.add_result(test_name_this, status, report_url, duration, bug_link)
            raise e
        finally:
            duration = time.time() - start_time
            collector.add_result(test_name_this, status, report_url, duration, bug_link)

    @pytest.mark.regress
    @pytest.mark.wish_tests
    def test_deflete_wish3(self):
        """Удаление желания"""
        test_name_this = "Удаление желания"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        status = "🔴"
        collector = ResultCollector()
        main_page = MainPage(self.driver)
        auth = AuthController()
        start_time = time.time()  # Фиксируем время начала теста

        try:
            # Подготовка и выполнение теста
            auth.authenticate_and_delete_user(TestData.phone_friend1)
            auth.authenticate_and_register_user(TestData.phone_friend1, TestData.friend1_name, "11", "1111")
            main_page.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)
            time.sleep(2)
            main_page.add_two_wishes()
            main_page.click(TestData.BOTTOM_WISHES_BTN)
            time.sleep(5)
            main_page.click(TestData.MY_WISHES_FIRST_WISH)
            time.sleep(5)
            main_page.click(TestData.MY_WISHES_OPENED_WISH_EDIT_BUTTON)
            time.sleep(2)
            main_page.click(TestData.MY_WISHES_EDIT_DELETE_BUTTON)
            time.sleep(2)
            main_page.click(MainPage.DELETE_WISH)
            time.sleep(5)
            assert main_page.is_element_invisible(TestData.MY_WISHES_SECOND_WISH), \
                "NOTIFICATION_AVATAR_UPDATED is visible when it should not be!"

            report_url = self.driver.capabilities.get("testobject_test_report_url", "нет ссылки")

            status = "🟢"
        except Exception as e:
            status = "🔴"
            duration = time.time() - start_time
            main_page.exc_handle(test_name_this, report_url, e)
            collector.add_result(test_name_this, status, report_url, duration)
            raise
        finally:
            duration = time.time() - start_time
            collector.add_result(test_name_this, status, report_url, duration)

    @pytest.mark.wish_tests
    @pytest.mark.regress
    def test_add_wish_from_catalog_visible_all(self):
        """Добавление желания из каталога с видимостью Всем"""

        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = "Желания: Добавление желания из каталога с видимостью Всем"
        main_page_1 = MainPage(self.driver)
        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()
        test_ss_name = "test_add_wish_from_catalog_visible_all"

        with allure.step("Authenticate and delete users before the test"):
            # Аутентификация и удаление пользователей перед тестом
            auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
            auth_controller.authenticate_and_delete_user(TestData.phone_friend2)
            auth_controller.authenticate_and_delete_user(TestData.phone_friend3)

            auth_controller.authenticate_and_register_user(TestData.phone_friend1, TestData.friend1_name, "11", "1111")
            auth_controller.authenticate_and_register_user(TestData.phone_friend2, TestData.friend2_name, "12", "1111")
            auth_controller.authenticate_and_register_user(TestData.phone_friend3, TestData.friend3_name, "12", "1111")

        try:
            with allure.step("Authorize users and register new accounts"):
                # Авторизация пользователей и регистрация новых аккаунтов
                # time.sleep(20)
                main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)

            with allure.step("Navigate through catalog and add a wish"):
                # Проходим по каталогу и добавляем желание
                main_page_1.add_two_wishes()

            with allure.step("Verify wish visibility under second user"):
                # Проверяем видимость желания у второго пользователя
                time.sleep(1)
                main_page_1.logout(self.driver)
                main_page_1.exit_app_and_reopen()

                main_page_1.auth_by_phone(TestData.phone_friend3, TestData.confirm_code)
                time.sleep(5)
                main_page_1.is_element_visible(TestData.BOTTOM_FRIENDS_BTN_XP)
                main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)

                main_page_1.is_element_visible(TestData.CONTACTS_FRIEND_1)
                main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
                main_page_1.is_element_visible(TestData.friend_wish_first_wish)
                time.sleep(5)


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

    @pytest.mark.wish_tests
    @pytest.mark.regress
    @allure.feature("Wish")
    @allure.story("Добавление желания из каталога с видимостью 'Только мне'")
    def test_add_wish_from_catalog_visible_only_me(self):
        """Добавление желания из каталога с видимостью Только мне"""

        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = "Желания: Добавление желания из каталога с видимостью 'Только мне'"
        test_ss_name = "test_add_wish_from_catalog_visible_only_me"
        main_page_1 = MainPage(self.driver)

        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        try:
            # Authenticate and delete users before the test
            with allure.step("Аутентификация и удаление тестовых пользователей"):
                # Authenticate and delete users before the test
                auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
                auth_controller.authenticate_and_delete_user(TestData.phone_friend2)
                auth_controller.authenticate_and_delete_user(TestData.phone_friend3)
                auth_controller.authenticate_and_register_user(TestData.phone_friend1, "Firsty", "11", "1111")
                auth_controller.authenticate_and_register_user(TestData.phone_friend2, "Vtoroy", "12", "1111")
                auth_controller.authenticate_and_register_user(TestData.phone_friend3, "Treti", "13", "1111")

            with allure.step("Аутентификация пользователя и регистрация"):
                main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)


            # Add wish
            with allure.step("Навигация и выбор желания из каталога"):
                time.sleep(2)
                main_page_1.click(TestData.BOTTOM_CATALOG_BTN)
                # TelegramReport.send_tg("click(MainPage.CATALOG_BOTTOM_BUTTON_BOUNDS)")
                time.sleep(5)
                main_page_1.click(TestData.CATALOG_CATEGORIES_BTN)
                # TelegramReport.send_tg("CATALOG_CATEGORIES_BUTTON clicked on phone 1")
                time.sleep(5)
                main_page_1.click_by_uiautomator(TestData.CATEGORY_LIST_ITEM_1)
                # TelegramReport.send_tg("CATALOG_LIGHT_BUTTON clicked on phone 1")
                time.sleep(5)
                main_page_1.click(TestData.CATEGORY_ITEM_2)
                # TelegramReport.send_tg("goods_list_first_good clicked on phone 1")
                time.sleep(5)

            with allure.step("Добавление желания и настройка видимости 'Только мне'"):
                main_page_1.scroll_until_visible(self.driver, MainPage.ADD_TO_WISHES_BUTTON)
                time.sleep(2)
                main_page_1.click(MainPage.ADD_TO_WISHES_BUTTON)
                # TelegramReport.send_tg("ADD_TO_WISHES_BUTTON clicked on phone 1")
                time.sleep(2)
                main_page_1.click(MainPage.ADD_WISH_WITH_SETTINGS)
                time.sleep(2)
                # TelegramReport.send_tg("ADD_WISH_WITH_SETTINGS clicked on phone 1")
                main_page_1.click_by_uiautomator_desc_contains(MainPage.PRIVACY_ONLY_ME_DESC)
                time.sleep(2)
                main_page_1.click(MainPage.ADD_BUTTON)


            with allure.step("Проверка видимости желания для второго пользователя"):
                main_page_1.logout(self)
                time.sleep(2)
                main_page_1.auth_by_phone(TestData.phone_friend2, TestData.confirm_code)
                time.sleep(2)
                main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
                time.sleep(5)
                main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_2)
                time.sleep(5)
                assert main_page_1.is_element_invisible(TestData.friend_wish_first_wish)

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

    @pytest.mark.wish_tests
    @pytest.mark.regress
    @allure.feature("Добавление желания")
    @allure.story("Добавление желания из каталога с видимостью Некоторым")
    def test_add_wish_from_catalog_visible_some(self):
        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = "Желания: Добавление желания из каталога с видимостью Некоторым"
        test_ss_name = "test_add_wish_from_catalog_visible_some"
        main_page_1 = MainPage(self.driver)

        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        with allure.step("Аутентификация и удаление пользователей перед тестом"):
            auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
            auth_controller.authenticate_and_delete_user(TestData.phone_friend2)
            auth_controller.authenticate_and_delete_user(TestData.phone_friend3)
            auth_controller.authenticate_and_register_user(TestData.phone_friend1, TestData.friend1_name, "11", "1111")
            auth_controller.authenticate_and_register_user(TestData.phone_friend2, TestData.friend2_name, "12", "1111")
            auth_controller.authenticate_and_register_user(TestData.phone_friend3, TestData.friend3_name, "11", "1111")

        try:
            with allure.step("Регистрация пользователей"):
                time.sleep(5)
                main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)
                time.sleep(2)

            with allure.step("Проверка видимости кнопки настроек профиля"):
                assert main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR), \
                    "Profile settings button not visible!"
                # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")

            with allure.step("Обновление списка контактов"):
                time.sleep(2)
                main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
                time.sleep(5)
                main_page_1.swipe_down(999)
                time.sleep(2)
                main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
                time.sleep(2)
                main_page_1.swipe_down(999)
                time.sleep(2)

            with allure.step("Добавление желания из каталога"):
                time.sleep(2)
                main_page_1.click(TestData.BOTTOM_CATALOG_BTN)
                # TelegramReport.send_tg("click(MainPage.CATALOG_BOTTOM_BUTTON_BOUNDS)")
                time.sleep(2)
                main_page_1.click(TestData.CATALOG_CATEGORIES_BTN)
                # TelegramReport.send_tg("CATALOG_CATEGORIES_BUTTON clicked on phone 1")
                time.sleep(2)
                main_page_1.click_by_uiautomator(TestData.CATEGORY_LIST_ITEM_1)
                # TelegramReport.send_tg("CATALOG_LIGHT_BUTTON clicked on phone 1")
                time.sleep(2)
                main_page_1.click(TestData.CATEGORY_ITEM_2)
                # TelegramReport.send_tg("goods_list_first_good clicked on phone 1")
                time.sleep(5)
                main_page_1.scroll_until_visible(self.driver, MainPage.ADD_TO_WISHES_BUTTON)
                time.sleep(2)
                main_page_1.click(MainPage.ADD_TO_WISHES_BUTTON)
                # TelegramReport.send_tg("ADD_TO_WISHES_BUTTON clicked on phone 1")
                time.sleep(2)

            with allure.step("Выбор видимости Некоторым"):
                main_page_1.click(MainPage.ADD_WISH_WITH_SETTINGS)
                time.sleep(2)
                # TelegramReport.send_tg("ADD_WISH_WITH_SETTINGS clicked on phone 1")
                main_page_1.click_by_uiautomator_desc_contains(MainPage.PRIVACY_SOME_DESC)
                time.sleep(4)
                main_page_1.click_by_uiautomator_desc_contains(TestData.choose_friends_first)
                time.sleep(2)
                main_page_1.click(MainPage.DONE_BUTTON)
                time.sleep(2)
                main_page_1.click(MainPage.ADD_BUTTON)

            with allure.step("Проверка уведомления о добавлении желания"):
                self.assertTrue(
                    main_page_1.is_element_visible(MainPage.NOTIFICATION_WISH_ADDED),
                    "NOTIFICATION_WISH_SUGGESTED not visible!"
                )
                self.assertTrue(
                    main_page_1.is_element_invisible(MainPage.NOTIFICATION_WISH_ADDED),
                    "NOTIFICATION_WISH_SUGGESTED visible!"
                )

            with allure.step("Проверка видимости желания под вторым пользователем"):
                time.sleep(2)
                main_page_1.logout(self.driver)
                time.sleep(2)
                main_page_1.auth_by_phone(TestData.phone_friend2, TestData.confirm_code)
                time.sleep(5)
                main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
                time.sleep(5)
                main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_2)
                time.sleep(5)



            with allure.step("Проверка отсутствия желания под третьим пользователем"):
                time.sleep(1)
                main_page_1.logout(self.driver)
                main_page_1.auth_by_phone(TestData.phone_friend3, TestData.confirm_code)
                main_page_1.is_element_visible(TestData.BOTTOM_FRIENDS_BTN_XP)
                main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
                main_page_1.is_element_visible(TestData.CONTACTS_FRIEND_2)
                main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_2)
                main_page_1.is_element_invisible(TestData.FRIEND_WISH_1)
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

    @pytest.mark.wish_tests
    @pytest.mark.regress
    def test_add_partner_wish_from_catalog_visible_all(self):
        """Добавление партнерского желания из каталога с видимостью Всем"""
        status = "🟡"
        bug_link = "/-/issues/3237"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = "Желания: Добавление партнерского желания из каталога с видимостью Всем"
        test_ss_name = "test_add_partner_wish_from_catalog_visible_all"
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
            with allure.step("Авторизация первого пользователя"):
                time.sleep(2)
                main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)

                # TelegramReport.send_tg("User 1 authenticated and registered")

            with allure.step("Проверка видимости кнопки профиля"):
                assert main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR), \
                    "Profile settings button not visible!"
                # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")

            # Add wish
            with allure.step("Переход в каталог и выбор товара"):
                time.sleep(2)
                main_page_1.click(TestData.BOTTOM_CATALOG_BTN)
                time.sleep(5)
                main_page_1.click(TestData.catalog_search_field)
                time.sleep(2)
                main_page_1.send_keys_simple(TestData.partner_wish)
                time.sleep(2)
                main_page_1.click(TestData.catalog_search_field_result)
                time.sleep(5)
                main_page_1.click_by_uiautomator(TestData.CATEGORY_ITEM_1)
                time.sleep(2)
                main_page_1.scroll_until_visible(self.driver, MainPage.ADD_TO_WISHES_OR_BUY_BUTTON)
                time.sleep(2)
                main_page_1.click(MainPage.ADD_TO_WISHES_OR_BUY_BUTTON)
                time.sleep(2)
                main_page_1.click(TestData.partner_wish_add_button)
                # self.assertTrue(
                #     main_page_1.is_element_visible(MainPage.NOTIFICATION_WISH_ADDED),
                #     "NOTIFICATION_WISH_SUGGESTED not visible!"
                # )
                # self.assertTrue(
                #     main_page_1.is_element_invisible(MainPage.NOTIFICATION_WISH_ADDED),
                #     "NOTIFICATION_WISH_SUGGESTED not visible!"
                # )

                # Проверка под вторым юзером
                main_page_1.logout(self.driver)
                main_page_1.auth_by_phone(TestData.phone_friend2, TestData.confirm_code)
                main_page_1.open_first_friend_first_wish()

            status = "🟢"
        except Exception as e:
            status = "🟡"
            duration = time.time() - start_time
            collector.add_result(test_name_this, status, report_url, duration, bug_link)
            raise e
        finally:
            duration = time.time() - start_time
            collector.add_result(test_name_this, status, report_url, duration, bug_link)

    @pytest.mark.wish_tests
    @pytest.mark.regress
    def test_add_partner_wish_from_catalog_visible_only_me(self):
        """BUG: ждем ID /-/issues/2287"""
        status = "🟡"
        bug_link = "/-/issues/2287"
        #status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = "Добавление PARTNER желания из каталога с видимостью Только мне"
        test_ss_name = "test_add_partner_wish_from_catalog_visible_only_me"
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
            time.sleep(20)
            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)
            time.sleep(2)

            main_page_1.register_new_user(self.driver, TestData.phone_friend2)

            assert main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR), \
                "Profile settings button not visible!"
            # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")

            # Шаг 1: добавление желания
            with allure.step("Нажатие кнопки нижнего меню каталога"):
                time.sleep(2)
                main_page_1.click(TestData.BOTTOM_CATALOG_BTN)
                # TelegramReport.send_tg("click(MainPage.CATALOG_BOTTOM_BUTTON_BOUNDS)")
                time.sleep(5)

            # Шаг 2: поиск и выбор товара
            with allure.step("Выбор товара через строку поиска каталога"):
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

            # Шаг 3: добавление в желания
            with allure.step("Прокрутка до кнопки добавления в желания"):
                main_page_1.scroll_until_visible(self.driver, MainPage.ADD_TO_WISHES_OR_BUY_BUTTON)
                time.sleep(2)
                main_page_1.click(MainPage.ADD_TO_WISHES_OR_BUY_BUTTON)
                # TelegramReport.send_tg("ADD_TO_WISHES_BUTTON clicked on phone 1")
                time.sleep(2)

            # Шаг 4: добавление PARTNER с настройками
            with allure.step("Добавление PARTNER желания с настройками"):
                main_page_1.click_element_by_bounds(TestData.partner_wish_add_with_settings_button)
                time.sleep(2)
                main_page_1.click(TestData.partner_wish_add_button)
                time.sleep(2)

            # Шаг 5: выбор приватности "Только мне"
            with allure.step("Выбор приватности Только мне"):
                main_page_1.click_by_uiautomator_desc_contains(MainPage.PRIVACY_ONLY_ME_DESC)
                time.sleep(2)
                main_page_1.click(MainPage.ADD_BUTTON)

            # Шаг 6: проверка уведомления о добавлении желания
            #with allure.step("Проверка отображения уведомления о добавлении желания"):
                # self.assertTrue(
                #     main_page_1.is_element_visible(MainPage.NOTIFICATION_WISH_ADDED),
                #     "NOTIFICATION_WISH_SUGGESTED not visible!"
                # )
                # self.assertTrue(
                #     main_page_1.is_element_invisible(MainPage.NOTIFICATION_WISH_ADDED),
                #     "NOTIFICATION_WISH_SUGGESTED not visible!"
                # )

            # Шаг 7: Проверка видимости под вторым пользователем
            with allure.step("Проверка видимости желания под вторым пользователем"):
                # Проверка под вторым юзером
                main_page_1.logout(self.driver)
                main_page_1.auth_by_phone(TestData.phone_friend2, TestData.confirm_code)
                main_page_1.open_first_friend_first_wish()

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

    @pytest.mark.wish_tests
    @pytest.mark.regress
    def test_add_partner_wish_from_catalog_visible_some(self):
        """BUG: ждем ID /-/issues/2287"""

        status = "🔴"
        status = "🟡"
        bug_link = "/-/issues/2287"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = "Добавление PARTNER желания из каталога с видимостью Некоторым"
        test_ss_name = "test_add_partner_wish_from_catalog_visible_some"
        main_page_1 = MainPage(self.driver)

        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        # Authenticate and delete users before the test
        auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend2)
        auth_controller.authenticate_and_register_user(TestData.phone_friend1, "Firsty", "11", "1111")
        auth_controller.authenticate_and_register_user(TestData.phone_friend2, "Vtoroy", "12", "1111")
        auth_controller.authenticate_and_delete_user(TestData.phone_friend3)
        auth_controller.authenticate_and_register_user(TestData.phone_friend3, TestData.friend3_name, "12", "1111")
        try:
            # Auth
            time.sleep(20)
            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)
            time.sleep(2)

            main_page_1.register_new_user(self.driver, TestData.phone_friend2)

            assert main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR), \
                "Profile settings button not visible!"
            # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")

            # Refresh contacts for first user
            with allure.step("Обновление контактов первого пользователя"):
                time.sleep(2)
                main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
                time.sleep(2)
                main_page_1.swipe_down(999)
                time.sleep(2)

            # Refresh contacts for second user
            with allure.step("Обновление контактов второго пользователя"):
                time.sleep(2)
                main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
                time.sleep(2)
                main_page_1.swipe_down(999)
                time.sleep(2)

            # Add wish from catalog
            with allure.step("Добавление желания из каталога"):
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
                main_page_1.scroll_until_visible(self.driver, MainPage.ADD_TO_WISHES_OR_BUY_BUTTON)
                time.sleep(2)
                main_page_1.click(MainPage.ADD_TO_WISHES_OR_BUY_BUTTON)
                # TelegramReport.send_tg("ADD_TO_WISHES_BUTTON clicked on phone 1")
                time.sleep(2)

            # Add partner wish with settings
            with allure.step("Добавление желания партнера с настройками"):
                main_page_1.click_element_by_bounds(TestData.partner_wish_add_with_settings_button)
                time.sleep(2)
                main_page_1.click(TestData.partner_wish_add_button)
                time.sleep(2)

            # Select privacy option "Some"
            with allure.step("Выбор видимости Некоторым"):
                main_page_1.click_by_uiautomator_desc_contains(MainPage.PRIVACY_SOME_DESC)
                time.sleep(4)

            # Select first friend
            with allure.step("Выбор первого друга"):
                main_page_1.click_by_uiautomator_desc_contains(TestData.choose_friends_first)
                time.sleep(2)

            # Click Done
            with allure.step("Нажатие кнопки Готово"):
                main_page_1.click(MainPage.DONE_BUTTON)
                time.sleep(2)

            # Click Add
            with allure.step("Нажатие кнопки Добавить"):
                main_page_1.click(MainPage.ADD_BUTTON)
                time.sleep(2)

            # Check notification
            #with allure.step("Проверка отображения уведомления"):
                # self.assertTrue(
                #     main_page_1.is_element_visible(MainPage.NOTIFICATION_WISH_ADDED),
                #     "NOTIFICATION_WISH_SUGGESTED not visible!"
                # )
                # self.assertTrue(
                #     main_page_1.is_element_invisible(MainPage.NOTIFICATION_WISH_ADDED),
                #     "NOTIFICATION_WISH_SUGGESTED visible!"
                # )

            # Check with second user
            with allure.step("Проверка отображения под вторым пользователем"):
                main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
                time.sleep(2)
                main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
                time.sleep(2)

                # Screenshot for second user
                action_taken = "_wish_visible_under_phone2"
                ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
                ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
                time.sleep(1)
                assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Logout second user and login third user
            with allure.step("Разлогинивание второго пользователя и вход третьим"):
                time.sleep(2)
                main_page_1.logout(self.driver)
                time.sleep(2)

                main_page_1.auth_by_phone(TestData.phone_friend3, TestData.confirm_code)
                time.sleep(2)
                main_page_1.register_new_user(self.driver, TestData.phone_friend2)
                time.sleep(2)

            # Check with third user
            with allure.step("Проверка отображения под третьим пользователем"):
                main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
                time.sleep(2)
                main_page_1.swipe_down(999)
                time.sleep(4)
                main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
                time.sleep(4)

                # Screenshot for third user
                action_taken = "_wish_not_visible_under_phone3"
                ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
                ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
                time.sleep(1)
                assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

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

    @pytest.mark.wish_tests
    @pytest.mark.regress
    def test_add_partner_wish_from_catalog_description_filled(self):
        """Добавление partner_ желания из каталога с дополнительным описанием"""

        status = "🟡"
        bug_link = "/-/issues/3237"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = "Добавление partner_ желания из каталога с дополнительным описанием"
        test_ss_name = "test_add_partner_wish_from_catalog_description_filled"
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
            time.sleep(2)

            assert main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR), \
                "Profile settings button not visible!"
            # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")

            # Добавление желания
            with allure.step("Нажатие кнопки нижнего меню каталога"):
                time.sleep(2)
                main_page_1.click(TestData.BOTTOM_CATALOG_BTN)
                # TelegramReport.send_tg("click(MainPage.CATALOG_BOTTOM_BUTTON_BOUNDS)")
            time.sleep(5)

            with allure.step("Выбор поля поиска каталога"):
                main_page_1.click(TestData.catalog_search_field)
                # TelegramReport.send_tg("CATALOG_CATEGORIES_BUTTON clicked on phone 1")
            time.sleep(2)

            with allure.step("Ввод текста поиска партнёрского желания"):
                main_page_1.send_keys_simple(TestData.partner_wish)
            time.sleep(2)

            with allure.step("Выбор результата поиска"):
                main_page_1.click(TestData.catalog_search_field_result)
            time.sleep(5)

            with allure.step("Выбор товара"):
                main_page_1.click_by_uiautomator(TestData.CATEGORY_ITEM_1)
                # TelegramReport.send_tg("goods_list_first_good clicked on phone 1")
            time.sleep(2)

            with allure.step("Прокрутка до кнопки добавления в желания"):
                main_page_1.scroll_until_visible(self.driver, MainPage.ADD_TO_WISHES_OR_BUY_BUTTON)
                time.sleep(2)
                main_page_1.click(MainPage.ADD_TO_WISHES_OR_BUY_BUTTON)
                # TelegramReport.send_tg("ADD_TO_WISHES_BUTTON clicked on phone 1")
            time.sleep(2)

            # добавление PARTNER с настройками
            with allure.step("Нажатие кнопки добавления желания с настройками"):
                main_page_1.click_element_by_bounds(TestData.partner_wish_add_with_settings_button)
            time.sleep(2)

            with allure.step("Нажатие кнопки добавления партнёрского желания"):
                main_page_1.click(TestData.partner_wish_add_button)
            time.sleep(2)

            # описание
            with allure.step("Ввод описания желания из каталога"):
                main_page_1.click(TestData.wish_from_catalog_description_field)
            time.sleep(2)
            main_page_1.copy_paste_simple(TestData.long_description)
            time.sleep(2)

            with allure.step("Нажатие кнопки добавления желания"):
                main_page_1.click(MainPage.ADD_BUTTON)
            time.sleep(2)

            # Проверка отображения
            with allure.step("Просмотр списка желаемых товаров"):
                main_page_1.click(TestData.BOTTOM_WISHES_BTN)
            time.sleep(2)
            main_page_1.click_by_uiautomator(TestData.MY_WISHES_FIRST_WISH)
            time.sleep(2)
            main_page_1.swipe_up(1500)
            time.sleep(2)


            time.sleep(2)
            main_page_1.click_element_by_bounds(TestData.added_wish_details_of_description_button)
            time.sleep(2)


            time.sleep(2)
            main_page_1.swipe_up(1500)
            time.sleep(3)

            status = "🟢"
        except Exception as e:
            status = "🟡"
            duration = time.time() - start_time
            collector.add_result(test_name_this, status, report_url, duration, bug_link)
            raise e
        finally:
            duration = time.time() - start_time
            collector.add_result(test_name_this, status, report_url, duration, bug_link)
