import re
import time
import traceback

from selenium.webdriver.support import expected_conditions as EC

import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

import ResultCollector
from core.pages.main_page import MainPage
from core.data.test_data import TestData
from reporting.TelegramReport import TelegramReport
from core.api.AuthController import AuthController
from core.pages.base_test import BaseTest
from ResultCollector import ResultCollector
import pytest
import allure
import time


class PaymentTests(BaseTest):
    @pytest.mark.regress
    @pytest.mark.payment_tests
    @allure.story("Test Case: Полная оплата подарка на котором уже есть накопления")
    def test_complete_payment_for_existing_donated_wish(self):
        #TelegramReport.send_tg("START 0")
        status = "🟡"
        bug_link = "/-/issues/3237"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = "Оплата: Полная оплата подарка на котором уже есть накопления"
        test_ss_name = "test_complete_payment_for_existing_donated_wish"
        main_page_1 = MainPage(self.driver)
        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        # Authenticate and delete users before the test
        auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        auth_controller.authenticate_and_register_user(TestData.phone_friend1, TestData.friend1_name, "11", "1111")

        try:
            # Auth
            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)

            # Добавление желания
            main_page_1.add_two_wishes()

            # donate to gift 1
            with allure.step("Просмотр списка желаемых товаров"):
                time.sleep(5)
                main_page_1.click(TestData.BOTTOM_WISHES_BTN)
                # TelegramReport.send_tg("click(MainPage.CATALOG_BOTTOM_BUTTON_BOUNDS)")
                time.sleep(5)
                main_page_1.click_by_uiautomator(TestData.MY_WISHES_FIRST_WISH)
                # main_page_1.click_by_uiautomator(TestData.my_wish_first_wish)
                time.sleep(6)

            with allure.step("Прокрутка до кнопки оплаты желания"):
                main_page_1.scroll_until_visible(self.driver, MainPage.PAY_FOR_WISH_BUTTON)
                time.sleep(5)
                main_page_1.click(MainPage.PAY_FOR_WISH_BUTTON)
                # TelegramReport.send_tg("PAY_FOR_WISH_BUTTON clicked on phone 1")

            with allure.step("Ввод суммы оплаты"):
                time.sleep(5)
                main_page_1.click_by_uiautomator(TestData.PAYMENT_DONATE_MONEY_AMOUNT_FIELD)
                # TelegramReport.send_tg("click(MainPage.payment_money_amount_filed)")
                time.sleep(2)
                main_page_1.send_keys_simple("100")
                time.sleep(2)
                self.driver.hide_keyboard()
                time.sleep(1)

            with allure.step("Оплатить"):
                main_page_1.scroll_until_visible(self.driver, MainPage.PAY_GO_TO_PAYMENT_BUTTON)
                time.sleep(2)
                main_page_1.click(MainPage.PAY_GO_TO_PAYMENT_BUTTON)
                # TelegramReport.send_tg("PAY_GO_TO_PAYMENT_BUTTON clicked on phone 1")

            # PAY
            main_page_1.pay_by_card()

            # donate to gift 2
            with allure.step("Просмотр списка желаемых товаров"):
                time.sleep(5)
                main_page_1.click(TestData.BOTTOM_WISHES_BTN)
                # TelegramReport.send_tg("click(MainPage.CATALOG_BOTTOM_BUTTON_BOUNDS)")
                time.sleep(5)
                main_page_1.click_by_uiautomator(TestData.MY_WISHES_FIRST_WISH)
                time.sleep(6)

            with allure.step("Прокрутка до кнопки оплаты желания"):
                main_page_1.scroll_until_visible(self.driver, MainPage.PAY_FOR_WISH_BUTTON)
                time.sleep(5)
                main_page_1.click(MainPage.PAY_FOR_WISH_BUTTON)
                # TelegramReport.send_tg("PAY_FOR_WISH_BUTTON clicked on phone 1")

            with allure.step("Ввод суммы оплаты"):
                time.sleep(5)
                main_page_1.is_element_visible(TestData.PAYMENT_DONATE_SET_FULL_AMOUNT_BTN)
                main_page_1.click_by_uiautomator(TestData.PAYMENT_DONATE_SET_FULL_AMOUNT_BTN)
                # TelegramReport.send_tg("click(MainPage.payment_money_amount_filed)")
                time.sleep(2)

            with allure.step("Оплатить"):
                main_page_1.scroll_until_visible(self.driver, MainPage.PAY_GO_TO_PAYMENT_BUTTON)
                time.sleep(2)
                main_page_1.click(MainPage.PAY_GO_TO_PAYMENT_BUTTON)

            # PAY
            main_page_1.pay_by_card()
            time.sleep(30)
            main_page_1.is_element_visible(TestData.BOTTOM_WISHES_BTN)
            main_page_1.click(TestData.BOTTOM_WISHES_BTN)
            main_page_1.scroll_until_visible(self.driver, TestData.WISHES_100_FULL)
            main_page_1.is_element_visible(TestData.WISHES_100_FULL)

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
    @pytest.mark.payment_tests
    @allure.story("Тест: Добавление желания из каталога и частичная оплата")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_wish_partial_payment(self):
        """Добавление желания из каталога и частичная оплата"""
        #TelegramReport.send_tg("START 1")

        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = "Оплата: Добавление желания из каталога и частичная оплата"
        test_ss_name = "test_wish_partial_payment"
        main_page_1 = MainPage(self.driver)
        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        # Authenticate and delete users before the test
        auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        auth_controller.authenticate_and_register_user(TestData.phone_friend1, "Firsty", "20", "1111")

        try:
            # Auth
            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)
            # Добавление желания
            main_page_1.add_two_wishes()

            # donate to gift
            with allure.step("Просмотр списка желаемых товаров"):
                time.sleep(5)
                main_page_1.click(TestData.BOTTOM_WISHES_BTN)
                time.sleep(5)
                main_page_1.click_by_uiautomator(TestData.MY_WISHES_FIRST_WISH)
                time.sleep(6)

            with allure.step("Прокрутка до кнопки оплаты желания"):
                main_page_1.scroll_until_visible(self.driver, MainPage.PAY_FOR_WISH_BUTTON)
                time.sleep(5)
                main_page_1.click(MainPage.PAY_FOR_WISH_BUTTON)

            with allure.step("Ввод суммы оплаты"):
                time.sleep(5)
                main_page_1.click_by_uiautomator(TestData.PAYMENT_DONATE_MONEY_AMOUNT_FIELD)
                time.sleep(2)
                main_page_1.send_keys_simple("100")
                time.sleep(2)
                self.driver.hide_keyboard()

            with allure.step("Оплатить"):
                main_page_1.scroll_until_visible(self.driver, MainPage.PAY_GO_TO_PAYMENT_BUTTON)
                time.sleep(2)
                main_page_1.click(MainPage.PAY_GO_TO_PAYMENT_BUTTON)

            # PAY
            main_page_1.pay_by_card()

            # Screenshot block
            time.sleep(2)
            action_taken = "_wish_payed_confirm"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            with allure.step("Снимок экрана с эталонным изображением подтверждения оплаты желания"):
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
                allure.attach.file(ss_etalon, name="Etalon Screenshot", attachment_type=allure.attachment_type.PNG)
            with allure.step("Снимок экрана с результатом выполнения теста подтверждения оплаты желания"):
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


    @pytest.mark.regress
    @pytest.mark.payment_tests
    @allure.story("Test Case: Добавление желания из каталога и полная оплата с доставкой")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_wish_and_complete_payment_with_delivery(self):
        """Добавление желания из каталога и полная оплата с доставкой"""
        #TelegramReport.send_tg("START 2")
        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = "Оплата: Добавление желания из каталога и полная оплата с доставкой"
        test_ss_name = "test_add_wish_and_complete_payment_with_delivery"
        main_page_1 = MainPage(self.driver)
        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        # Инициализируем ResultCollector до try/except
        collector = ResultCollector()

        # Authenticate and delete users before the test
        time.sleep(20)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        auth_controller.authenticate_and_register_user(TestData.phone_friend1, "Firsty", "20", "1111")
        auth_controller.authenticate_and_delete_user(TestData.phone_friend2)
        auth_controller.authenticate_and_register_user(TestData.phone_friend2, "Vtoroy", "40", "1111")

        try:
            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)
            # Добавление желания
            main_page_1.add_two_wishes()

            # Полная оплата с доставкой
            with allure.step("Переход в список желаемых товаров"):
                time.sleep(3)
                main_page_1.click(TestData.BOTTOM_WISHES_BTN)

            with allure.step("Выбор первого желания"):
                time.sleep(5)
                main_page_1.click_by_uiautomator(TestData.MY_WISHES_FIRST_WISH)

            with allure.step("Прокрутка до кнопки 'Оплатить'"):
                time.sleep(3)
                main_page_1.scroll_until_visible(self.driver, MainPage.PAY_FOR_WISH_BUTTON)
                time.sleep(2)
                main_page_1.click(MainPage.PAY_FOR_WISH_BUTTON)

            with allure.step("Исполнить чекбокс"):
                time.sleep(3)
                main_page_1.click_by_uiautomator(TestData.PAYMENT_CHOOSE_FULL_PAYMENT_OPTION)

            with allure.step("Исполнить снизу кнопка"):
                time.sleep(2)
                main_page_1.scroll_until_visible(self.driver, MainPage.PAYMENT_EXECUTE_BUTTON)
                time.sleep(2)
                main_page_1.click(MainPage.PAYMENT_EXECUTE_BUTTON)

            # Доставка
            with allure.step("Выбор получателя"):
                time.sleep(3)
                main_page_1.click_by_uiautomator(TestData.DELIVERY_CHOOSE_RECIPIENT)
                time.sleep(3)
                main_page_1.click_by_uiautomator(TestData.RECIPIENT_CHOOSE_USER)
                time.sleep(3)
                main_page_1.click(MainPage.DONE_BUTTON)
                time.sleep(3)

            with allure.step("Выбор адреса доставки"):
                time.sleep(3)
                main_page_1.click_by_uiautomator(TestData.DELIVERY_CHOOSE_PICKUP_POINT)
                time.sleep(5)
                main_page_1.turn_on_gps()
                main_page_1.click_by_uiautomator(TestData.DELIVERY_PICKUP_POINT_SEARCH_FIELD)
                time.sleep(3)
                main_page_1.copy_paste_simple("Москва 2-й хвостов переулок 12")
                time.sleep(4)
                main_page_1.click_by_uiautomator(TestData.DELIVERY_PICKUP_POINT_SEARCH_RESULT_1)
                time.sleep(6)
                main_page_1.click(MainPage.DELIVERY_FOUND_SELECTED_PICKUP_POINT_CHOOSE_BUTTON)

            with allure.step("Переход к оплате с доставкой"):
                time.sleep(4)
                main_page_1.scroll_until_visible(self.driver, MainPage.PAY_GO_TO_PAYMENT_BUTTON)
                main_page_1.click(MainPage.PAY_GO_TO_PAYMENT_BUTTON)

            # Шаги с картой
            with allure.step("оплатa card"):
                main_page_1.pay_by_card()

            # Screenshot блок
            time.sleep(4)
            action_taken = "_payment_complete"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)

            with allure.step("Снимок экрана с эталонным изображением завершенной оплаты"):
                MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
                allure.attach.file(ss_etalon, name="Etalon Screenshot", attachment_type=allure.attachment_type.PNG)
            with allure.step("Снимок экрана с результатом выполнения теста (оплата завершена)"):
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


    @pytest.mark.regress
    @pytest.mark.payment_tests
    def test_friend_wish_partial_payment(self):
        """Частичная оплата желания друга"""
        #TelegramReport.send_tg("START 3")
        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = "Оплата: Частичная оплата желания друга"
        test_ss_name = "test_friend_wish_partial_payment"
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

            # Добавление желания
            main_page_1.add_two_wishes()

            main_page_1.logout(self)
            # Auth 2
            main_page_1.auth_by_phone(TestData.phone_friend2, TestData.confirm_code)

            # Открываем желание друга
            with allure.step("Открытие желания друга"):
                main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
                time.sleep(2)
                main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
                time.sleep(2)
                main_page_1.swipe_up(800)
                time.sleep(2)
                main_page_1.click(TestData.FRIEND_WISH_1)
                time.sleep(2)

            # Донат на подарок
            with allure.step("Донат на подарок"):
                time.sleep(2)
                main_page_1.scroll_until_visible(self.driver, MainPage.CONTRIBUTE_FOR_WISH_BUTTON)
                time.sleep(2)
                main_page_1.click(MainPage.CONTRIBUTE_FOR_WISH_BUTTON)
                time.sleep(2)
                main_page_1.click_by_uiautomator(TestData.PAYMENT_DONATE_MONEY_AMOUNT_FIELD)
                time.sleep(2)
                main_page_1.send_keys_simple("100")
                time.sleep(1)
                self.driver.hide_keyboard()
                time.sleep(1)
                main_page_1.scroll_until_visible(self.driver, MainPage.PAY_GO_TO_PAYMENT_BUTTON)
                time.sleep(2)
                main_page_1.click(MainPage.PAY_GO_TO_PAYMENT_BUTTON)

                main_page_1.pay_by_card()

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
    @pytest.mark.payment_tests
    @allure.story("Test Case: Оплата желаний друга, которые предложил пользователь полная оплата")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_suggest_wish_and_complete_payment_with_delivery(self):
        """Тест для оплаты желаний друга, предложенных пользователем, с полной оплатой"""
        #TelegramReport.send_tg("START 4")
        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url",
                                                  "недоступен")  # Изначально результат теста - успех
        test_ss_name = "test_suggest_wish_and_complete_payment_with_delivery"  # Имя теста
        test_name_this = "Оплата: Желание друга, которое предложил пользователь: Полная оплата"
        main_page_1 = MainPage(self.driver)  # Страница для первого пользователя

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

            main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),

            main_page_1.suggest_wish_to_friend_1()
            main_page_1.suggest_wish_to_friend_1()

            main_page_1.logout(self.driver)
            main_page_1.auth_by_phone(TestData.phone_friend3, TestData.confirm_code)

            #main_page_1.accept_first_wish_privacy_all()
            main_page_1.accept_two_wish_privacy_all()

            # Блок снимков экрана
            action_taken = "_after_wish_add_phone1"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            main_page_1.logout(self.driver)
            main_page_1.auth_by_phone(TestData.phone_friend1, TestData.confirm_code)

            main_page_1.open_first_friend_first_wish()

            with allure.step("Прокрутка до кнопки 'Оплатить'"):
                time.sleep(3)
                main_page_1.scroll_until_visible(self.driver, MainPage.CONTRIBUTE_FOR_WISH_BUTTON)
                time.sleep(2)
                main_page_1.click(MainPage.CONTRIBUTE_FOR_WISH_BUTTON)

            with allure.step("Исполнить чекбокс"):
                time.sleep(3)
                main_page_1.click_by_uiautomator(TestData.PAYMENT_CHOOSE_FULL_PAYMENT_OPTION)

            with allure.step("Исполнить снизу кнопка"):
                time.sleep(2)
                main_page_1.scroll_until_visible(self.driver, MainPage.PAYMENT_EXECUTE_BUTTON)
                time.sleep(2)
                main_page_1.click(MainPage.PAYMENT_EXECUTE_BUTTON)

            # Доставка
            with allure.step("Выбор получателя"):
                time.sleep(3)
                main_page_1.click_by_uiautomator(TestData.DELIVERY_CHOOSE_RECIPIENT)
                time.sleep(3)
                main_page_1.click_by_uiautomator(TestData.RECIPIENT_CHOOSE_USER)
                time.sleep(3)
                main_page_1.click(MainPage.DONE_BUTTON)
                time.sleep(3)

            with allure.step("Выбор адреса доставки"):
                time.sleep(3)
                main_page_1.click_by_uiautomator(TestData.DELIVERY_CHOOSE_PICKUP_POINT)
                time.sleep(5)
                main_page_1.turn_on_gps()
                time.sleep(5)
                main_page_1.click_by_uiautomator(TestData.DELIVERY_PICKUP_POINT_SEARCH_FIELD)
                time.sleep(3)
                main_page_1.copy_paste_simple("Москва 2-й хвостов переулок 12")
                time.sleep(4)
                main_page_1.click_by_uiautomator(TestData.DELIVERY_PICKUP_POINT_SEARCH_RESULT_1)
                time.sleep(6)
                main_page_1.click(MainPage.DELIVERY_FOUND_SELECTED_PICKUP_POINT_CHOOSE_BUTTON)

            with allure.step("Переход к оплате с доставкой"):
                time.sleep(4)
                main_page_1.scroll_until_visible(self.driver, MainPage.PAY_GO_TO_PAYMENT_BUTTON)
                main_page_1.click(MainPage.PAY_GO_TO_PAYMENT_BUTTON)

            # Шаги с картой
            with allure.step("оплатa card"):
                main_page_1.pay_by_card()

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
    @pytest.mark.payment_tests
    def test_suggest_wish_then_partial_and_full_payment_with_receive(self):
        """BUG: /-/issues/3237"""
        #status = "🔴"
        status = "🟡"
        bug_link = "/-/issues/3237"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = "Оплата: Желание друга, которое предложил пользователь: Полная оплата с двух аккаунтов и Получение желания с доставкой в ПВ"
        test_ss_name = "test_suggest_wish_then_partial_and_full_payment_with_receive"
        main_page_1 = MainPage(self.driver)

        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        # Authenticate and delete users before the test
        auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend2)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend3)
        auth_controller.authenticate_and_register_user(TestData.phone_friend1, "Firsty_NEW", "11", "1111")
        auth_controller.authenticate_and_register_user(TestData.phone_friend2, "Vtoroy_NEW", "12", "1111")
        auth_controller.authenticate_and_register_user(TestData.phone_friend3, "Treti_NEW", "13", "1111")

        try:
            # Auth 1
            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)
            main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),
            main_page_1.suggest_wish_to_friend_1()
            main_page_1.suggest_wish_to_friend_1()
            main_page_1.logout(self.driver)

            # Auth 3
            main_page_1.auth_by_phone(TestData.phone_friend3, TestData.confirm_code)
            main_page_1.accept_two_wish_privacy_all()
            main_page_1.logout(self.driver)

            # Auth 2
            main_page_1.auth_by_phone(TestData.phone_friend2, TestData.confirm_code)

            # Открываем желание друга
            main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
            time.sleep(2)
            main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_2)
            time.sleep(2)
            main_page_1.swipe_up(800)
            time.sleep(2)
            main_page_1.click(TestData.FRIEND_WISH_1)
            time.sleep(2)

            # Донат на подарок
            time.sleep(2)
            main_page_1.scroll_until_visible(self.driver, MainPage.CONTRIBUTE_FOR_WISH_BUTTON)
            time.sleep(2)
            main_page_1.click(MainPage.CONTRIBUTE_FOR_WISH_BUTTON)
            time.sleep(2)
            main_page_1.click_by_uiautomator(TestData.PAYMENT_DONATE_MONEY_AMOUNT_FIELD)
            time.sleep(2)
            main_page_1.send_keys_simple("100")
            time.sleep(1)
            self.driver.hide_keyboard()
            time.sleep(1)
            main_page_1.scroll_until_visible(self.driver, MainPage.PAY_GO_TO_PAYMENT_BUTTON)
            time.sleep(2)
            main_page_1.click(MainPage.PAY_GO_TO_PAYMENT_BUTTON)

            main_page_1.pay_by_card()
            main_page_1.logout(self.driver)

            # Auth 1
            main_page_1.auth_by_phone(TestData.phone_friend1, TestData.confirm_code)
            main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),

            # Открываем желание друга
            main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
            time.sleep(2)
            main_page_1.click_by_uiautomator(TestData.CONTACTS_FRIEND_1)
            time.sleep(2)
            main_page_1.swipe_up(800)
            time.sleep(2)
            main_page_1.click(TestData.FRIEND_WISH_1)
            time.sleep(2)
            # Донат на подарок
            time.sleep(2)
            main_page_1.scroll_until_visible(self.driver, MainPage.CONTRIBUTE_FOR_WISH_BUTTON)
            time.sleep(2)
            main_page_1.click(MainPage.CONTRIBUTE_FOR_WISH_BUTTON)
            time.sleep(2)
            main_page_1.click_by_uiautomator(TestData.PAYMENT_DONATE_SET_FULL_AMOUNT_BTN)
            time.sleep(2)
            main_page_1.scroll_until_visible(self.driver, MainPage.PAY_GO_TO_PAYMENT_BUTTON)
            time.sleep(2)
            main_page_1.click(MainPage.PAY_GO_TO_PAYMENT_BUTTON)

            main_page_1.pay_by_card()
            main_page_1.logout(self.driver)

            # Auth 3
            main_page_1.auth_by_phone(TestData.phone_friend3, TestData.confirm_code)
            main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR),

            main_page_1.click(TestData.BOTTOM_WISHES_BTN)
            main_page_1.is_element_visible(TestData.WISHES_100_FULL)
            main_page_1.click(TestData.WISHES_100_FULL)

            main_page_1.scroll_until_visible(self.driver, TestData.receive_wish)
            main_page_1.is_element_visible(TestData.receive_wish)
            main_page_1.click(TestData.receive_wish)


            # Доставка
            with allure.step("Выбор получателя"):
                time.sleep(3)
                main_page_1.is_element_visible(TestData.DELIVERY_CHOOSE_RECIPIENT)
                main_page_1.click_by_uiautomator(TestData.DELIVERY_CHOOSE_RECIPIENT)
                time.sleep(3)
                main_page_1.click_by_uiautomator(TestData.RECIPIENT_CHOOSE_USER)
                time.sleep(3)
                main_page_1.click(MainPage.DONE_BUTTON)
                time.sleep(3)

            with allure.step("Выбор адреса доставки"):
                time.sleep(3)
                main_page_1.click_by_uiautomator(TestData.DELIVERY_CHOOSE_PICKUP_POINT)
                time.sleep(5)
                main_page_1.turn_on_gps()
                time.sleep(5)
                main_page_1.click_by_uiautomator(TestData.DELIVERY_PICKUP_POINT_SEARCH_FIELD)
                time.sleep(3)
                main_page_1.copy_paste_simple("Москва 2-й хвостов переулок 12")
                time.sleep(4)
                main_page_1.click_by_uiautomator(TestData.DELIVERY_PICKUP_POINT_SEARCH_RESULT_1)
                time.sleep(6)
                main_page_1.click(MainPage.DELIVERY_FOUND_SELECTED_PICKUP_POINT_CHOOSE_BUTTON)

            with allure.step("Переход к оплате с доставкой"):
                time.sleep(4)
                main_page_1.scroll_until_visible(self.driver, MainPage.PAY_GO_TO_PAYMENT_BUTTON)
                main_page_1.click(MainPage.PAY_GO_TO_PAYMENT_BUTTON)
                main_page_1.pay_by_card()

                main_page_1.is_element_visible(TestData.BOTTOM_WISHES_BTN)
                main_page_1.click(TestData.BOTTOM_WISHES_BTN)
                main_page_1.is_element_visible(TestData.WISH_IS_COMPLETING)
                main_page_1.click(TestData.WISH_IS_COMPLETING)

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