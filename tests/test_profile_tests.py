import re
import time
import traceback

import pytest
import allure

from ResultCollector import ResultCollector
from core.pages.main_page import MainPage
from core.data.test_data import TestData
from reporting.TelegramReport import TelegramReport
from core.api.AuthController import AuthController
from core.pages.base_test import BaseTest


class ProfileTests(BaseTest):
    @pytest.mark.regress
    @pytest.mark.profile_tests
    @allure.story("Test Case: Setting Avatar")
    @allure.severity(allure.severity_level.NORMAL)
    def test_set_avatar(self):
        """Установка аватара пользователю"""

        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = "Профиль Пользователя: Установка аватара пользователю"
        test_ss_name = "test_set_avatar"
        main_page_1 = MainPage(self.driver)
        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        # Authenticate and delete users before the test
        auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        auth_controller.authenticate_and_register_user(TestData.phone_friend1, TestData.friend1_name, "11", "1111")

        try:
            # Auth
            main_page_1.upload_image_to_device("tests/pictures/DSC00062.jpg", "/sdcard/Download/DSC00062.jpg")
            time.sleep(2)
            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)
            main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR)
            main_page_1.click_by_uiautomator(MainPage.PROFILE_SETTINGS_LOCATOR)
            time.sleep(3)
            main_page_1.click_by_uiautomator(TestData.avatar_bonds)
            time.sleep(3)
            main_page_1.click(TestData.downloads_bonds)
            time.sleep(3)
            main_page_1.click(TestData.pictue_first_pic_from_gallery)
            time.sleep(5)
            main_page_1.click(MainPage.DONE_BUTTON)

            main_page_1.is_element_visible(MainPage.NOTIFICATION_AVATAR_UPDATED)

            status = "🟢"
        except Exception as e:
            status = "🔴"
            duration = time.time() - start_time
            #main_page_1.exc_handle(test_name_this, report_url, e)
            collector.add_result(test_name_this, status, report_url, duration)
            raise
        finally:
            duration = time.time() - start_time
            collector.add_result(test_name_this, status, report_url, duration)

    @pytest.mark.profile_tests
    @allure.story("Test Case: Смена аватара пользователю")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_avatar(self):
        """Смена аватара пользователю"""

        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = ""
        test_ss_name = "test_update_avatar"
        main_page_1 = MainPage(self.driver)
        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        # Authenticate and delete users before the test
        auth_controller.authenticate_and_delete_user(TestData.phone_friend3)

        try:
            # Auth
            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend3, TestData.confirm_code)
            main_page_1.register_new_user(self.driver, TestData.phone_friend3)

            assert main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR), \
                "Profile settings button not visible!"
            # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")

            main_page_1.click_by_uiautomator(MainPage.PROFILE_SETTINGS_LOCATOR)
            time.sleep(3)

            # Установка аватара
            with allure.step("Нажатие на аватар для установки"):
                main_page_1.click_by_uiautomator(TestData.avatar_bonds)
                time.sleep(3)
                main_page_1.click_element_by_bounds(TestData.downloads_bonds)
                time.sleep(3)
                main_page_1.click_element_by_bounds(TestData.pictue_first_pic_from_gallery)
                time.sleep(3)
                main_page_1.click(MainPage.DONE_BUTTON)

            # Проверяем, что уведомление пришло и ушло
            with allure.step("Проверка отображения уведомления о смене аватара"):
                assert main_page_1.is_element_visible(MainPage.NOTIFICATION_AVATAR_UPDATED), \
                    "NOTIFICATION_AVATAR_UPDATED not visible!"
                # TelegramReport.send_tg("NOTIFICATION_AVATAR_UPDATED visible main_page_1")
                assert main_page_1.is_element_invisible(MainPage.NOTIFICATION_AVATAR_UPDATED), \
                    "NOTIFICATION_AVATAR_UPDATED is visible when it should not be!"

            # Screenshot block
            action_taken = "_after_set_avatar"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            allure.attach.file(ss_etalon, name="Etalon Screenshot", attachment_type=allure.attachment_type.PNG)
            allure.attach.file(ss_run, name="Run Screenshot", attachment_type=allure.attachment_type.PNG)
            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"

            # Обновление аватара
            with allure.step("Нажатие на аватар для обновления"):
                main_page_1.click_by_uiautomator(TestData.avatar_bonds)
                time.sleep(3)
                main_page_1.click_element_by_bounds(TestData.update_avatar_bonds)
                time.sleep(3)
                main_page_1.click_element_by_bounds(TestData.downloads_bonds)
                time.sleep(3)
                main_page_1.click_element_by_bounds(TestData.picture_for_update_avatar_bonds)
                time.sleep(3)
                main_page_1.click(MainPage.DONE_BUTTON)

            # Проверяем, что уведомление пришло и ушло
            with allure.step("Проверка отображения уведомления о смене аватара"):
                assert main_page_1.is_element_visible(MainPage.NOTIFICATION_AVATAR_UPDATED), \
                    "NOTIFICATION_AVATAR_UPDATED not visible!"
                # TelegramReport.send_tg("NOTIFICATION_AVATAR_UPDATED visible main_page_1")
                assert main_page_1.is_element_invisible(MainPage.NOTIFICATION_AVATAR_UPDATED), \
                    "NOTIFICATION_AVATAR_UPDATED is visible when it should not be!"

            # Screenshot block
            action_taken = "_after_update_avatar"
            ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
            ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
            MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
            allure.attach.file(ss_etalon, name="Etalon Screenshot", attachment_type=allure.attachment_type.PNG)
            allure.attach.file(ss_run, name="Run Screenshot", attachment_type=allure.attachment_type.PNG)
            time.sleep(1)
            assert MainPage.compare_screenshots(ss_run, ss_etalon), "Image comparison failed"
            status = "🟢"
        except Exception as e:
            test_result = "🟥"
            TelegramReport.send_tg(f"{test_result}  \n Error during test execution: {str(e)}")
            raise e  # Ensure test failure is raised and recognized
        finally:
            time.sleep(1)
            TelegramReport.send_tg(f"{test_result} ")

    @pytest.mark.regress
    @pytest.mark.profile_tests
    @allure.story("Test Case: Обновление данных профиля")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_edit_personal_info(self):
        """Обновление данных профиля"""

        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = "Профиль Пользователя: Обновление данных профиля"
        test_ss_name = "test_edit_personal_info"
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
            time.sleep(2)
            main_page_1.click_by_uiautomator(MainPage.PROFILE_SETTINGS_LOCATOR)
            time.sleep(3)

            main_page_1.click_by_uiautomator(TestData.PERSONAL_PROFILE_PERSONAL_DATA)
            time.sleep(2)
            main_page_1.click_by_uiautomator(TestData.PERSONAL_DATA_NAME)
            time.sleep(2)
            main_page_1.clear_text_field()
            time.sleep(2)
            main_page_1.send_keys_simple("Pervaya")
            time.sleep(2)
            main_page_1.click_by_uiautomator(TestData.PERSONAL_DATA_SECOND_NAME)
            time.sleep(1)
            main_page_1.clear_text_field()
            time.sleep(1)
            main_page_1.send_keys_simple("Egorova")
            time.sleep(1)
            main_page_1.click_by_uiautomator(TestData.PERSONAL_DATA_CHOOSE_GENDER)
            time.sleep(1)
            main_page_1.click(TestData.profile_gender_female_bonds)
            time.sleep(2)
            main_page_1.click_by_uiautomator(TestData.PERSONAL_DATA_BIRTH_DAY_DATE)
            time.sleep(2)
            main_page_1.clear_text_field()
            main_page_1.send_keys_simple("12122000")
            main_page_1.click(MainPage.DONE_BUTTON)

            # Validate notification
            self.assertTrue(
                main_page_1.is_element_visible(MainPage.NOTIFICATION_PROFILE_DATA_UPDATED),
                "NOTIFICATION_PROFILE_DATA_UPDATED not visible!"
            )
            self.assertTrue(
                main_page_1.is_element_invisible(MainPage.NOTIFICATION_PROFILE_DATA_UPDATED),
                "NOTIFICATION_PROFILE_DATA_UPDATED not invisible!"
            )

            time.sleep(2)
            main_page_1.is_element_visible(TestData.UPDATED_PROFILE_NAME)
            main_page_1.is_element_visible(TestData.UPDATED_PROFILE_BIRTH_DAY)


            status = "🟢"
        except Exception as e:
            status = "🔴"
            duration = time.time() - start_time
            #main_page_1.exc_handle(test_name_this, report_url, e)
            collector.add_result(test_name_this, status, report_url, duration)
            raise
        finally:
            duration = time.time() - start_time
            collector.add_result(test_name_this, status, report_url, duration)

    @pytest.mark.regress
    @pytest.mark.profile_tests
    @allure.story("Тест: Удаление профиля без активных желаний")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_profile_without_wish(self):
        """bug:/-/issues/3329"""

        #status = "🔴"
        status = "🟡"
        bug_link = "/-/issues/3329"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_ss_name = "test_delete_profile_without_wish"
        test_name_this = "Профиль Пользователя: Удаление профиля без активных желаний"
        main_page_1 = MainPage(self.driver)
        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        # Authenticate and delete users before the test
        auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        auth_controller.authenticate_and_register_user(TestData.phone_friend1, "Firsty", "11", "1111")

        try:
            # Auth
            with allure.step("Авторизация с помощью телефона"):
                main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)

                # TelegramReport.send_tg("Авторизация прошла успешно")

            assert main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR), \
                "Profile settings button not visible!"
            # TelegramReport.send_tg("PROFILE_SETTINGS_LOCATOR visible")

            with allure.step("Переход в настройки профиля"):
                main_page_1.click_by_uiautomator(MainPage.PROFILE_SETTINGS_LOCATOR)
                time.sleep(3)

            with allure.step("Прокрутка страницы вверх"):
                main_page_1.swipe_up(1600)
                # TelegramReport.send_tg("swipe_up(600)")
                time.sleep(1)

            with allure.step("Выбор личных данных"):
                main_page_1.click(TestData.personal_data_bonds)
                time.sleep(1)

            with allure.step("Нажатие на кнопку удаления профиля"):
                main_page_1.click(TestData.profile_delete_profile_bonds)
                time.sleep(1)

            with allure.step("Подтверждение удаления профиля"):
                main_page_1.click(TestData.profile_delete_confirm_bonds)
                time.sleep(5)
                main_page_1.is_element_visible(TestData.COME_IN)

            status = "🟢"
        except Exception as e:
            #status = "🔴"
            status = "🟡"
            duration = time.time() - start_time
            #main_page_1.exc_handle(test_name_this, report_url, e)
            collector.add_result(test_name_this, status, report_url, duration, bug_link)
            raise
        finally:
            duration = time.time() - start_time
            collector.add_result(test_name_this, status, report_url, duration, bug_link)

    @pytest.mark.profile_tests
    @pytest.mark.regress
    def test_delete_profile_with_active_wish(self):
        """BUG: /-/issues/3329"""

        #status = "🔴"
        status = "🟡"
        bug_link = "/-/issues/3329"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = "Удаление профиля когда есть желания на которых есть накопления"
        test_ss_name = "test_delete_profile_without_wish"
        main_page_1 = MainPage(self.driver)
        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        # Authenticate and delete users before the test
        auth_controller.authenticate_and_delete_user(TestData.phone_friend_no_delete)
        auth_controller.authenticate_and_register_user(TestData.phone_friend_no_delete, TestData.friend1_name, "11", "1111")

        try:
            # Auth
            time.sleep(20)
            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend_no_delete, TestData.confirm_code)

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



            time.sleep(2)
            main_page_1.click_by_uiautomator(MainPage.PROFILE_SETTINGS_LOCATOR)
            time.sleep(3)
            main_page_1.swipe_up(1600)
            # TelegramReport.send_tg("swipe_up(600)")
            time.sleep(1)
            main_page_1.click(TestData.personal_data_bonds)
            time.sleep(1)
            main_page_1.click(TestData.profile_delete_profile_bonds)
            time.sleep(1)
            main_page_1.click(TestData.profile_delete_confirm_bonds)



            status = "🟢"
        except Exception as e:
            #status = "🔴"
            status = "🟡"
            duration = time.time() - start_time
            #main_page_1.exc_handle(test_name_this, report_url, e)
            collector.add_result(test_name_this, status, report_url, duration, bug_link)
            raise
        finally:
            duration = time.time() - start_time
            collector.add_result(test_name_this, status, report_url, duration, bug_link)

    @pytest.mark.regress
    @pytest.mark.profile_tests
    @allure.story("Test Case: Отправка письма в поддержку")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_send_support_message(self):
        """Отправка письма в поддержку"""

        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = "Профиль Пользователя: Отправка письма в поддержку"
        test_ss_name = "test_send_support_message"
        main_page_1 = MainPage(self.driver)
        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        # Authenticate and delete users before the test
        auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        auth_controller.authenticate_and_register_user(TestData.phone_friend1, TestData.friend1_name, "11", "1111")

        try:
            # Auth
            with allure.step("Аутентификация пользователя"):
                main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)

            with allure.step("Открытие настроек профиля"):
                main_page_1.click_by_uiautomator(MainPage.PROFILE_SETTINGS_LOCATOR)
                time.sleep(3)

            with allure.step("Прокрутка страницы"):
                main_page_1.swipe_up(1600)
                # TelegramReport.send_tg("swipe_up(1600)")
                time.sleep(1)

            with allure.step("Нажатие на кнопку помощи"):
                main_page_1.click(TestData.profile_help_button_bonds)
                time.sleep(2)

            with allure.step("Заполнение поля с email"):
                main_page_1.click(TestData.profile_help_email_tf)
                time.sleep(2)
                main_page_1.send_keys_simple("e2e_test_proj@proton.me")
                self.driver.hide_keyboard()
                time.sleep(2)

            with allure.step("Заполнение поля с темой"):
                main_page_1.click(TestData.profile_help_tema_tf)
                time.sleep(2)
                main_page_1.send_keys_simple("pamagiteee")
                self.driver.hide_keyboard()
                time.sleep(2)

            with allure.step("Заполнение поля с сообщением"):
                main_page_1.click(TestData.profile_help_message_tf)
                time.sleep(2)
                main_page_1.send_keys_simple("pomogite pojalusta ya autotest")
                self.driver.hide_keyboard()
                time.sleep(2)

            with allure.step("Отправка сообщения"):
                main_page_1.click(MainPage.SEND_BUTTON)
                time.sleep(2)

            with allure.step("Проверка отображения уведомления о отправке сообщения"):
                self.assertTrue(
                    main_page_1.is_element_visible(MainPage.NOTIFICATION_SUPPORT_MESSAGE_SENT),
                    "NOTIFICATION_SUPPORT_MESSAGE_SENT not visible!"
                )
                self.assertTrue(
                    main_page_1.is_element_invisible(MainPage.NOTIFICATION_SUPPORT_MESSAGE_SENT),
                    "NOTIFICATION_SUPPORT_MESSAGE_SENT not invisible!"
                )
                # TelegramReport.send_tg("NOTIFICATION_SUPPORT_MESSAGE_SENT visible main_page_1")

            status = "🟢"
        except Exception as e:
            status = "🔴"
            duration = time.time() - start_time
            #main_page_1.exc_handle(test_name_this, report_url, e)
            collector.add_result(test_name_this, status, report_url, duration)
            raise
        finally:
            duration = time.time() - start_time
            collector.add_result(test_name_this, status, report_url, duration)

    @pytest.mark.regress
    @pytest.mark.profile_tests
    def test_send_feedback_message(self):
    #bug: /-/issues/3342

        #status = "🔴"

        status = "🟡"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = "Отправка обратной связи"
        test_ss_name = "test_send_feedback_message"
        main_page_1 = MainPage(self.driver)
        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()
        bug_link = "/-/issues/3342"

        # Authenticate and delete users before the test
        #auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        #auth_controller.authenticate_and_register_user(TestData.phone_friend1, TestData.friend1_name, "11", "1111")

        try:
            # Auth

            #main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)
            main_page_1.skip_onboarding()
            main_page_1.auth_by_phone(TestData.phone_friend1, TestData.confirm_code)


            main_page_1.is_element_visible(TestData.FEEDBACK_BTN)
            main_page_1.click(TestData.FEEDBACK_BTN)
            time.sleep(3)
            main_page_1.proceed_feedback()



            status = "🟢"
        except Exception as e:
            #status = "🔴"
            status = "🟡"
            duration = time.time() - start_time
            # main_page_1.exc_handle(test_name_this, report_url, e)
            collector.add_result(test_name_this, status, report_url, duration, bug_link)
            raise
        finally:
            duration = time.time() - start_time
            collector.add_result(test_name_this, status, report_url, duration, bug_link)