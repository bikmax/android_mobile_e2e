import logging
import os
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
from tools.get_email_code import get_confirmation_code

"""
Run tests: python tests/runner.py notifications_tests
"""


class Notifications(BaseTest):
    # @pytest.mark.notifications_tests
    # def test_notification_new_friend_in_app(self):
    #     """Новый друг в приложении (Для пользователей с таким номеров в контактах)"""
    #     status = "🟢"
    #     test_ss_name = "test_suggest_gift_to_friend_and_accept_privacy_all"
    #     main_page_1 = MainPage(self.driver)
    #     main_page_1 = MainPage(self.driver)
    #     auth_controller = AuthController()
    #
    #     # Authenticate and delete users before the test
    #     auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
    #     auth_controller.authenticate_and_delete_user(TestData.phone_friend2)
    #
    #     try:
    #         # Auth
    #         main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)
    #         
    #         main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend2, TestData.confirm_code)
    #         main_page_1.register_new_user(self.driver, TestData.phone_friend2)
    #
    #         self.assertTrue(
    #             main_page_1.is_element_visible(MainPage.NOTIFICATION_NEW_FRIEND_IN_APP),
    #             "NOTIFICATION_WISH_SUGGESTED not visible!"
    #         )
    #         self.assertTrue(
    #             main_page_1.is_element_invisible(MainPage.NOTIFICATION_NEW_FRIEND_IN_APP),
    #             "NOTIFICATION_WISH_SUGGESTED not visible!"
    #         )
    #         #TelegramReport.send_tg("NOTIFICATION_WISH_SUGGESTED visible main_page_1")
    #
    #         main_page_1.click(TestData.notification_bell)
    #         time.sleep(2)
    #         # Screenshot block
    #         action_taken = "_after_reg_check_friend_notif"
    #         ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
    #         ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
    #         MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
    #         MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
    #         time.sleep(1)
    #         assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"
    #
    #         main_page_1.click(MainPage.SEE_BUTTON)
    #         time.sleep(2)
    #         # Screenshot block
    #         action_taken = "_after_reg_check_friend_profile"
    #         ss_etalon = MainPage.generate_filename("etalon", action_taken, test_ss_name)
    #         ss_run = MainPage.generate_filename("run", action_taken, test_ss_name)
    #         MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_etalon)
    #         MainPage.take_element_screenshot_by_bounds(self.driver, TestData.main_screen_ss, ss_run)
    #         time.sleep(1)
    #         assert MainPage.compare_screenshots(ss_run, ss_etalon), f"Image comparison failed"
    #
    #     except Exception as e:
    #         test_result = "🟥"
    #         TelegramReport.send_tg(f"{test_result} {test_desc} \n Error during test execution: {str(e)}")
    #         raise e
    #     finally:
    #         TelegramReport.send_tg(f"{test_result} {test_desc}")

    @pytest.mark.regress
    @pytest.mark.notifications_tests
    def test_notification_friend_added_new_wish(self):
        """BUG: /-/issues/3157"""
        #status = "🔴"
        status = "🟡"
        bug_link = "/-/issues/3157"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = "Уведомления: Создание желания. Просмотр желания другом через уведомления"
        test_ss_name = "test_gift_friend_privacy_all"
        main_page_1 = MainPage(self.driver)

        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        # Authenticate and delete users before the test
        auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend2)
        auth_controller.authenticate_and_delete_user(TestData.phone_friend3)
        auth_controller.authenticate_and_register_user(TestData.phone_friend1, "Firsty", "11", "1111")
        auth_controller.authenticate_and_register_user(TestData.phone_friend3, "Treti", "11", "1111")
        auth_controller.authenticate_and_register_user(TestData.phone_friend2, "Vtoroy", "12", "1111")

        try:
            # Auth
            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)

            main_page_1.add_two_wishes()

            main_page_1.logout(self)
            main_page_1.exit_app_and_reopen()

            main_page_1.auth_by_phone(TestData.phone_friend3, TestData.confirm_code)

            main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)
            main_page_1.is_element_visible(TestData.CONTACTS_FRIEND_1)
            main_page_1.click(TestData.BOTTOM_HOME_BTN_XP)

            main_page_1.is_element_visible(TestData.notification_bell_have_1)
            # TelegramReport.send_tg("SEE notification_bell")
            main_page_1.click(TestData.notification_bell_have_1)
            # TelegramReport.send_tg("CLICK notification_bell")
            time.sleep(5)

            main_page_1.is_element_visible(MainPage.SEE_BUTTON)
            main_page_1.click(MainPage.SEE_BUTTON)
            time.sleep(5)

            # Проверяем то что желание открылось и видна кнопка Поучаствовать
            main_page_1.is_element_visible(MainPage.CONTRIBUTE_FOR_WISH_BUTTON)

            status = "🟢"
        except Exception as e:
            status = "🟡"
            #status = "🔴"
            duration = time.time() - start_time
            main_page_1.exc_handle(test_name_this, report_url, e)
            collector.add_result(test_name_this, status, report_url, duration, bug_link)
            raise
        finally:
            duration = time.time() - start_time
            collector.add_result(test_name_this, status, report_url, duration, bug_link)

    @pytest.mark.regress
    @pytest.mark.notifications_tests
    def test_suggest_gift_to_friend(self):
        """BUG: /-/issues/3157"""
        #status = "🔴"
        status = "🟡"
        bug_link = "/-/issues/3157"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = "Уведомления: Предложение подарка другу, принятие другом через уведомления, проверка получения уведомления другом который предложил желание"
        test_ss_name = "test_suggest_gift_to_friend"
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

            main_page_1.suggest_wish_to_friend_1()
            main_page_1.logout(self)
            main_page_1.exit_app_and_reopen()
            main_page_1.auth_by_phone(TestData.phone_friend3, TestData.confirm_code)

            main_page_1.is_element_visible(TestData.notification_bell_have_2)
            # TelegramReport.send_tg("SEE notification_bell")
            main_page_1.click(TestData.notification_bell_have_2)
            # TelegramReport.send_tg("CLICK notification_bell")
            time.sleep(5)

            main_page_1.is_element_visible(MainPage.SEE_BUTTON_1)
            main_page_1.click(MainPage.SEE_BUTTON_1)
            time.sleep(5)

            # Проверяем что видно кнопку Принять
            main_page_1.is_element_visible(MainPage.ACCEPT_WISH_BUTTON)

            main_page_1.accept_first_wish_privacy_all()
            main_page_1.logout(self)
            main_page_1.exit_app_and_reopen()
            main_page_1.auth_by_phone(TestData.phone_friend1, TestData.confirm_code)

            main_page_1.is_element_visible(TestData.notification_bell_have_1)
            # TelegramReport.send_tg("SEE notification_bell")
            main_page_1.click(TestData.notification_bell_have_1)
            # TelegramReport.send_tg("CLICK notification_bell")
            time.sleep(5)

            main_page_1.is_element_visible(MainPage.SEE_BUTTON_1)
            time.sleep(5)


            status = "🟢"
        except Exception as e:
            status = "🟡"
            #status = "🔴"
            duration = time.time() - start_time
            main_page_1.exc_handle(test_name_this, report_url, e)
            collector.add_result(test_name_this, status, report_url, duration, bug_link)
            raise
        finally:
            duration = time.time() - start_time
            collector.add_result(test_name_this, status, report_url, duration, bug_link)

    @pytest.mark.mergecheck
    @pytest.mark.notifications_tests
    def test_mergecheck(self):
        """mergecheck"""
        status = "🔴"  # По умолчанию считаем тест неуспешным
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = "merge check dev to rc"
        test_ss_name = "test_mergecheck"
        main_page_1 = MainPage(self.driver)

        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        # Получаем информацию о коммите и пайплайне
        raw_commit_message = os.getenv("CI_COMMIT_MESSAGE", "")
        commit_title = os.getenv("CI_COMMIT_TITLE", "N/A")
        project_url = os.getenv("CI_PROJECT_URL",
                                "https://gitlab.com/e2e_test_proj-e2e-development/e2e_test_proj/mobile/e2e_test_proj_mobile")
        pipeline_id = os.getenv("CI_PIPELINE_ID", "unknown")
        pipeline_url = f"{project_url}/-/pipelines/{pipeline_id}"
        branch_name = os.getenv("CI_COMMIT_REF_NAME", "unknown branch")
        source_branch = os.getenv("CI_MERGE_REQUEST_SOURCE_BRANCH_NAME", "?")
        target_branch = os.getenv("CI_MERGE_REQUEST_TARGET_BRANCH_NAME", "?")

        try:
            # Authenticate and delete users before the test
            auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
            auth_controller.authenticate_and_delete_user(TestData.phone_friend2)
            auth_controller.authenticate_and_delete_user(TestData.phone_friend3)
            auth_controller.authenticate_and_register_user(TestData.phone_friend1, "Firsty", "11", "1111")
            auth_controller.authenticate_and_register_user(TestData.phone_friend2, "Vtoroy", "12", "1111")
            auth_controller.authenticate_and_register_user(TestData.phone_friend3, "Treti", "13", "1111")

            # Основные шаги теста
            main_page_1.auth_by_phone_with_skip_ob(TestData.phone_friend1, TestData.confirm_code)

            main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR)
            main_page_1.click_by_uiautomator(MainPage.PROFILE_SETTINGS_LOCATOR)

            main_page_1.is_element_visible(TestData.PROFILE_SETTINGS_USERNUMBER_MERGE)

            main_page_1.add_two_wishes()

            main_page_1.is_element_visible(TestData.BOTTOM_WISHES_BTN)
            main_page_1.click(TestData.BOTTOM_WISHES_BTN)

            main_page_1.is_element_visible(TestData.MY_WISHES_FIRST_WISH)

            main_page_1.is_element_visible(TestData.BOTTOM_FRIENDS_BTN_XP)
            main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)

            main_page_1.is_element_visible(TestData.CONTACTS_FRIEND_1)

            # Если дошли сюда без исключений - тест успешен
            status = "🟢"
            duration = time.time() - start_time

            # Формируем и отправляем сообщение об успехе
            success_msg = (
                f"✅ <b>MERGE CHECK УСПЕШЕН</b>\n"
                f"<b>Тест:</b> {test_name_this}\n"
                f"🌿<b>Ветка:</b> {source_branch} → {target_branch}\n"
                f"<b>Коммит:</b> {commit_title}\n"
                f"⏱ <b>Длительность:</b> {duration:.2f} сек\n"
                f" {TelegramReport.format_link('Ссылка на Пайплайн', pipeline_url)}"
            )
            TelegramReport.send_tg(success_msg)

        except Exception as e:
            duration = time.time() - start_time
            full_trace = traceback.format_exc()
            # Убираем лишние переносы строк и дублирование в сообщении
            error_lines = full_trace.split('\n')

            error_msg = (
                f"❌ <b>Тест упал:</b> {test_name_this}\n"
                f"<b>Ошибка:</b> {str(e)}\n"
                f"🌿 <b>Ветка:</b> {source_branch} → {target_branch}\n"
                f"<b>Коммит:</b> {commit_title}\n"
                f"⏱ <b>Длительность:</b> {duration:.2f} сек\n"
                f"🔗 {TelegramReport.format_link('Отчёт', report_url) if report_url != 'недоступен' else 'Отчёт недоступен'}\n"
                f"{TelegramReport.format_link('Пайплайн', pipeline_url)}"
            )

            #TelegramReport.send_tg(error_msg)
            raise e  # Пробрасываем исключение дальше для правильного отчета в pytest

        finally:
            # В блоке finally только сбор результатов и очистка
            duration = time.time() - start_time
            collector.add_result(test_name_this, status, report_url, duration)

            # Формируем итоговый отчет
            final_report = (
                f"<b>Итоговый отчёт</b>\n\n"
                f"1. {'🔴' if status == '🔴' else '🟢'} {test_name_this} "
                f"{TelegramReport.format_link('Отчёт', report_url) if report_url != 'недоступен' else ''}\n\n"
            )

            TelegramReport.send_tg(final_report)

    @pytest.mark.alivecheck
    @pytest.mark.notifications_tests
    @allure.story("Test Case: test_aliveprodcheck")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_aliveprodcheck(self):
        status = "🔴"  # По умолчанию считаем тест неуспешным
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = "PROD ALIVE CHECK UI"
        test_ss_name = "test_aliveprodcheck"
        main_page_1 = MainPage(self.driver)

        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        # Получаем информацию о коммите и пайплайне
        project_url = os.getenv("CI_PROJECT_URL",
                                "https://gitlab.com/e2e_test_proj-e2e-development/e2e_test_proj/mobile/e2e_test_proj_mobile")
        pipeline_id = os.getenv("CI_PIPELINE_ID", "unknown")
        pipeline_url = f"{project_url}/-/pipelines/{pipeline_id}"

        try:
            # Подготовка тестовых данных
            # auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
            # auth_controller.authenticate_and_register_user(TestData.phone_friend1, "Firsty", "11", "1111")

            # time.sleep(20)
            auth_controller.prod_authenticate_and_delete_user(TestData.phone_friend_alive)
            # auth_controller.authenticate_and_register_user(TestData.phone_friend_alive, "Firsty", "11", "1111")

            # Основные шаги теста
            main_page_1.skip_onboarding()
            main_page_1.auth_by_phone(TestData.phone_friend_alive, TestData.confirm_code)
            main_page_1.register_new_user_all_fields(self.driver, "aliveFirsty", "Petrov", "e2e_test_proj@proton.me")

            #main_page_1.is_element_visible(MainPage.PROFILE_SETTINGS_LOCATOR)
            #main_page_1.click_by_uiautomator(MainPage.PROFILE_SETTINGS_LOCATOR)

            #main_page_1.is_element_visible(TestData.PROFILE_SETTINGS_USERNUMBER)
            #time.sleep(2)
            #main_page_1.click(TestData.BOTTOM_HOME_BTN_XP)
            main_page_1.add_two_wishes()

            main_page_1.is_element_visible(TestData.BOTTOM_WISHES_BTN)
            main_page_1.click(TestData.BOTTOM_WISHES_BTN)

            main_page_1.is_element_visible(TestData.MY_WISHES_FIRST_WISH)

            main_page_1.is_element_visible(TestData.BOTTOM_FRIENDS_BTN_XP)
            main_page_1.click(TestData.BOTTOM_FRIENDS_BTN_XP)

            #main_page_1.is_element_visible(TestData.NO_FRIENDS)

            main_page_1.click(TestData.BOTTOM_HOME_BTN_XP)
            main_page_1.delete_user()
            main_page_1.auth_by_phone(TestData.phone_friend_alive, TestData.confirm_code)

            main_page_1.is_element_visible(MainPage.CONTINUE_BUTTON_LOCATOR)


            # Если дошли сюда без исключений - тест успешен
            status = "🟢"

        except Exception as e:

            duration = time.time() - start_time
            error_msg = (
                f"❌ <b>Тест упал:</b> {test_name_this}\n"
                f"<b>Ошибка:</b> {str(e)}\n"
                f"⏱ <b>Длительность:</b> {duration:.2f} сек\n"
                f"🔗 {TelegramReport.format_link('Отчёт', report_url) if report_url != 'недоступен' else 'Отчёт недоступен'}\n"
                f"{TelegramReport.format_link('Пайплайн', pipeline_url)}"
            )

            TelegramReport.send_tg_alive_fail(error_msg)
            raise e

        finally:
            # В блоке finally только сбор результатов и очистка
            duration = time.time() - start_time
            collector.add_result(test_name_this, status, report_url, duration)

            # Формируем итоговый отчет
            final_report = (
                f"<b>Итоговый отчёт</b>\n\n"
                f"1. {'🔴' if status == '🔴' else '🟢'} {test_name_this} "
                f"{TelegramReport.format_link('Отчёт', report_url) if report_url != 'недоступен' else ''}\n\n"
                f"⏱️ Общее время выполнения: {duration:.2f} сек\n"
            )
            TelegramReport.send_tg_alive_positive(final_report)

    @pytest.mark.regress
    @pytest.mark.notifications_tests
    def test_notification_resend_code(self):
        """Кейс получения уведомления "Код успешно отправлен" """
        status = "🔴"
        report_url = self.driver.capabilities.get("testobject_test_report_url", "недоступен")
        test_name_this = "Уведомления: Получение уведомления Код успешно отправлен"
        test_ss_name = "test_notification_resend_code"
        main_page_1 = MainPage(self.driver)
        auth_controller = AuthController()
        start_time = time.time()
        collector = ResultCollector()

        # Authenticate and delete users before the test
        auth_controller.authenticate_and_delete_user(TestData.phone_friend1)
        # auth_controller.authenticate_and_register_user(TestData.phone_friend1, TestData.friend1_name, "11", "1111")

        try:
            # Auth
            with allure.step("Start Authentication Process"):
                time.sleep(2)
                main_page_1.skip_onboarding()
                main_page_1.is_element_visible(TestData.AUTH_PHONE_FIELD)
                main_page_1.click(TestData.AUTH_PHONE_FIELD)
                time.sleep(2)
                main_page_1.send_keys_simple(TestData.phone_friend1)
                time.sleep(2)
                main_page_1.click(MainPage.CONTINUE_BUTTON_LOCATOR)
                time.sleep(22)  # Simulating a waiting time for code input
                main_page_1.click(TestData.auth_resend_code)

            # Assertion for notification visibility
            with allure.step("Check resend code notification visibility"):
                assert main_page_1.is_element_visible(MainPage.NOTIFICATION_RESEND_CODE), \
                    "NOTIFICATION_RESEND_CODE not visible!"
                assert main_page_1.is_element_invisible(MainPage.NOTIFICATION_RESEND_CODE), \
                    "NOTIFICATION_RESEND_CODE not invisible!"
                # TelegramReport.send_tg("NOTIFICATION_RESEND_CODE visible main_page_1")

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
