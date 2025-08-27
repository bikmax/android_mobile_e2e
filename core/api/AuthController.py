from datetime import datetime, timedelta
import requests
import json
import logging
import uuid
from reporting.TelegramReport import TelegramReport
from core.data.test_data import TestData

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

# Enable HTTP requests logging
requests_log = logging.getLogger("urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

# Define your API endpoints
ENDPOINT_AUTH_CONFIRM = "/v1/auth/confirm"
ENDPOINT_AUTH = "/v1/auth"

# Define your base URLs
BASE_URL = "https://e2e_test_proj-gateway-service-dev2.e2e_test_proj.com"
BASE_URL_PROD = "https://api.e2e_test_proj.com"

class AuthController:
    def __init__(self):
        self.base_url = BASE_URL
        self.base_url_prod = BASE_URL_PROD
        self.endpoints = {
            'auth': ENDPOINT_AUTH,
            'auth_confirm': ENDPOINT_AUTH_CONFIRM
        }

    def api_auth_by_phonenumber(self, phone_number, confirm_code="999999", use_prod=False):
        """
        Authenticate the user by phone number in a single method.
        Handles the entire authentication flow, including token retrieval.

        :param phone_number: The phone number for authentication.
        :param confirm_code: The confirmation code received by phone (default is "1111").
        :param use_prod: Boolean to determine if production URL should be used.
        :return: A dictionary containing access and refresh tokens if successful, else None.
        """
        base_url = self.base_url_prod if use_prod else self.base_url
        confirm_token = self.get_confirm_token(phone_number, base_url)
        if not confirm_token:
            logger.error("Failed to get confirmToken.")
            return None

        if not self.confirm_user_auth(confirm_token, confirm_code, base_url):
            logger.error("Failed to confirm user authentication.")
            return None

        return self.get_tokens(confirm_token, base_url)

    def get_confirm_token(self, phone_number, base_url):
        """
        Request and retrieve the confirmToken by sending the phone number to the API.

        :param phone_number: The phone number for authentication.
        :param base_url: The base URL to use for the request.
        :return: The confirmToken or None if the request fails.
        """
        url = f"{base_url}{self.endpoints['auth_confirm']}"
        payload = {"phoneNumber": phone_number}
        headers = self.get_headers()

        logger.debug(f"Requesting confirm token for phone number: {phone_number}")
        logger.debug(f"Request Payload: {json.dumps(payload, indent=2)}")
        logger.debug(f"Request Headers: {json.dumps(headers, indent=2)}")

        response = requests.post(url, json=payload, headers=headers)

        logger.debug(f"Response Status Code: {response.status_code}")
        logger.debug(f"Response Body: {response.text}")

        if response.status_code in [200, 201]:
            return response.json().get("confirmToken")
        else:
            logger.error(f"Error getting confirmToken: {response.status_code} - {response.text}")
            return None

    def confirm_user_auth(self, confirm_token, confirm_code, base_url):
        """
        Confirm the user authentication by sending the confirmCode and confirmToken.

        :param confirm_token: The confirmToken received in the previous step.
        :param confirm_code: The confirmation code (default is "1111").
        :param base_url: The base URL to use for the request.
        :return: True if confirmation is successful, False otherwise.
        """
        url = f"{base_url}{self.endpoints['auth_confirm']}/{confirm_token}"
        payload = {"confirmCode": confirm_code}
        headers = self.get_headers()

        logger.debug(f"Confirming user with confirmToken: {confirm_token} and confirmCode: {confirm_code}")
        logger.debug(f"Request Payload: {json.dumps(payload, indent=2)}")
        logger.debug(f"Request Headers: {json.dumps(headers, indent=2)}")

        response = requests.patch(url, json=payload, headers=headers)

        logger.debug(f"Response Status Code: {response.status_code}")
        logger.debug(f"Response Body: {response.text}")

        if response.status_code == 204:
            logger.info("User confirmed successfully.")
            return True
        else:
            logger.error(f"Error confirming user: {response.status_code} - {response.text}")
            return False

    def get_tokens(self, confirm_token, base_url):
        """
        Retrieve the access and refresh tokens after successful user confirmation.

        :param confirm_token: The confirmToken received after confirming the user.
        :param base_url: The base URL to use for the request.
        :return: A dictionary containing accessToken and refreshToken if successful, else None.
        """
        url = f"{base_url}{self.endpoints['auth']}/{confirm_token}"
        headers = self.get_headers()

        logger.debug(f"Getting tokens with confirmToken: {confirm_token}")
        logger.debug(f"Request Headers: {json.dumps(headers, indent=2)}")

        response = requests.post(url, headers=headers)

        logger.debug(f"Response Status Code: {response.status_code}")
        logger.debug(f"Response Body: {response.text}")

        if response.status_code == 201:
            response_data = response.json()
            access_token = response_data.get("accessToken")
            refresh_token = response_data.get("refreshToken")
            if access_token and refresh_token:
                return {"accessToken": access_token, "refreshToken": refresh_token}
            else:
                logger.error("Tokens not found in response.")
                return None
        else:
            logger.error(f"Error getting tokens: {response.status_code} - {response.text}")
            return None

    def api_delete_user(self, access_token, use_prod=False):
        """
        Delete the user by sending a DELETE request with the access token.

        :param access_token: The access token of the user to be deleted.
        :param use_prod: Boolean to determine if production URL should be used.
        :return: The response object from the DELETE request.
        """
        base_url = self.base_url_prod if use_prod else self.base_url
        url = f"{base_url}{self.endpoints['auth']}"
        headers = self.get_headers()
        headers["Authorization"] = f"Bearer {access_token}"

        logger.debug(f"Deleting user with access token: {access_token}")
        logger.debug(f"Request Headers: {json.dumps(headers, indent=2)}")

        response = requests.delete(url, headers=headers)

        logger.debug(f"Response Status Code: {response.status_code}")
        logger.debug(f"Response Body: {response.text}")

        if response.status_code == 200:
            logger.info("User deleted successfully.")
        else:
            logger.error(f"Error deleting user: {response.status_code} - {response.text}")

        return response

    def get_headers(self):
        """
        Generate headers for the API request with a unique CorrelationID.

        :return: A dictionary containing the headers.
        """
        correlation_id = str(uuid.uuid4())
        return {
            "Accept-Language": "en",
            "CorrelationID": correlation_id,
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "application/json"
        }

    def authenticate_and_delete_user(self, phone_number, confirm_code="5555"):
        """
        Authenticate a user and delete them in a single method.

        :param phone_number: The phone number to authenticate and delete.
        :param confirm_code: The confirmation code received (default is "1111").
        :return: None (performs authentication and deletion).
        """
        tokens = self.api_auth_by_phonenumber(phone_number, confirm_code)
        if not tokens:
            logger.error(f"Authentication failed for {phone_number}.")
            return

        access_token = tokens['accessToken']
        logger.info(f"Access Token for {phone_number}: {access_token}")

        response = self.api_delete_user(access_token)
        if response.status_code == 200:
            logger.info(f"User {phone_number} deleted successfully.")
        else:
            logger.error(f"Failed to delete user {phone_number}.")

    def prod_authenticate_and_delete_user(self, phone_number, confirm_code="5555"):
        """
        Authenticate a user and delete them in a single method using production URL.

        :param phone_number: The phone number to authenticate and delete.
        :param confirm_code: The confirmation code received (default is "1111").
        :return: None (performs authentication and deletion).
        """
        tokens = self.api_auth_by_phonenumber(phone_number, confirm_code, use_prod=True)
        if not tokens:
            logger.error(f"Authentication failed for {phone_number} on production.")
            return

        access_token = tokens['accessToken']
        logger.info(f"Access Token for {phone_number} on production: {access_token}")

        response = self.api_delete_user(access_token, use_prod=True)
        if response.status_code == 200:
            logger.info(f"User {phone_number} deleted successfully on production.")
        else:
            logger.error(f"Failed to delete user {phone_number} on production.")

    def authenticate_and_register_user(self, phone_number, name, days_ahead, confirm_code="5555"):
        """
        Authenticate a user, register their profile, and update their contacts.

        :param phone_number: The phone number to authenticate and register.
        :param name: The name of the user.
        :param days_ahead: The number of days ahead from today to set the birthday.
        :param confirm_code: The confirmation code received (default is "1111").
        :return: None (performs authentication, profile registration, and contact update).
        """
        tokens = self.api_auth_by_phonenumber(phone_number, confirm_code)
        if not tokens:
            logger.error(f"Authentication failed for {phone_number}.")
            return

        access_token = tokens['accessToken']
        logger.info(f"Access Token for {phone_number}: {access_token}")

        today = datetime.today()
        birthday = today + timedelta(days=int(days_ahead))
        birthday_str = f"1970-{birthday.strftime('%m-%d')}"

        profile_updated = self.update_user_profile(access_token, name, birthday_str)
        if not profile_updated:
            logger.error(f"Failed to update profile for {phone_number}.")
            return

        contacts_updated = self.update_user_contacts(access_token, phone_number, name)
        if not contacts_updated:
            logger.error(f"Failed to update contacts for {phone_number}.")
            return

        get_user_contacts = self.get_user_contacts(access_token)
        if not get_user_contacts:
            logger.error(f"Failed to GET contacts for {phone_number}.")
            return

        logger.info(f"User {phone_number} registered and updated successfully.")

    def prod_authenticate_and_register_user(self, phone_number, name, days_ahead, confirm_code="5555"):
        """
        Authenticate a user, register their profile, and update their contacts using production URL.

        :param phone_number: The phone number to authenticate and register.
        :param name: The name of the user.
        :param days_ahead: The number of days ahead from today to set the birthday.
        :param confirm_code: The confirmation code received (default is "1111").
        :return: None (performs authentication, profile registration, and contact update).
        """
        tokens = self.api_auth_by_phonenumber(phone_number, confirm_code, use_prod=True)
        if not tokens:
            logger.error(f"Authentication failed for {phone_number} on production.")
            return

        access_token = tokens['accessToken']
        logger.info(f"Access Token for {phone_number} on production: {access_token}")

        today = datetime.today()
        birthday = today + timedelta(days=int(days_ahead))
        birthday_str = f"1970-{birthday.strftime('%m-%d')}"

        profile_updated = self.update_user_profile(access_token, name, birthday_str, use_prod=True)
        if not profile_updated:
            logger.error(f"Failed to update profile for {phone_number} on production.")
            return

        contacts_updated = self.update_user_contacts(access_token, phone_number, name, use_prod=True)
        if not contacts_updated:
            logger.error(f"Failed to update contacts for {phone_number} on production.")
            return

        get_user_contacts = self.get_user_contacts(access_token, use_prod=True)
        if not get_user_contacts:
            logger.error(f"Failed to GET contacts for {phone_number} on production.")
            return

        logger.info(f"User {phone_number} registered and updated successfully on production.")

    def authenticate_delete_and_register_user(self, phone_number, name, days_ahead, confirm_code="5555"):
        """
        Authenticate a user, delete them if they exist, and register a new user.

        :param phone_number: The phone number to authenticate and process.
        :param name: The name of the user.
        :param days_ahead: The number of days ahead from today to set the birthday.
        :param confirm_code: The confirmation code received (default is "1111").
        :return: None (performs authentication, deletion, registration, and updates).
        """
        tokens = self.api_auth_by_phonenumber(phone_number, confirm_code)
        if not tokens:
            logger.error(f"Authentication failed for {phone_number}.")
            return

        access_token = tokens['accessToken']
        logger.info(f"Access Token for {phone_number}: {access_token}")

        response = self.api_delete_user(access_token)
        if response.status_code == 200:
            logger.info(f"User {phone_number} deleted successfully.")
        else:
            logger.warning(f"Failed to delete user {phone_number}. Continuing with registration.")

        tokens = self.api_auth_by_phonenumber(phone_number, confirm_code)
        if not tokens:
            logger.error(f"Re-authentication failed for {phone_number} after deletion.")
            return

        access_token = tokens['accessToken']
        logger.info(f"New Access Token for {phone_number}: {access_token}")

        today = datetime.today()
        birthday = today + timedelta(days=int(days_ahead))
        birthday_str = f"1970-{birthday.strftime('%m-%d')}"

        if not self.update_user_profile(access_token, name, birthday_str):
            logger.error(f"Failed to update profile for {phone_number}.")
            return

        if not self.update_user_contacts(access_token, phone_number, name):
            logger.error(f"Failed to update contacts for {phone_number}.")
            return

        if not self.get_user_contacts(access_token):
            logger.error(f"Failed to GET contacts for {phone_number}.")
            return

        logger.info(f"User {phone_number} registered and updated successfully.")

    def prod_authenticate_delete_and_register_user(self, phone_number, name, days_ahead, confirm_code="5555"):
        """
        Authenticate a user, delete them if they exist, and register a new user using production URL.

        :param phone_number: The phone number to authenticate and process.
        :param name: The name of the user.
        :param days_ahead: The number of days ahead from today to set the birthday.
        :param confirm_code: The confirmation code received (default is "1111").
        :return: None (performs authentication, deletion, registration, and updates).
        """
        tokens = self.api_auth_by_phonenumber(phone_number, confirm_code, use_prod=True)
        if not tokens:
            logger.error(f"Authentication failed for {phone_number} on production.")
            return

        access_token = tokens['accessToken']
        logger.info(f"Access Token for {phone_number} on production: {access_token}")

        response = self.api_delete_user(access_token, use_prod=True)
        if response.status_code == 200:
            logger.info(f"User {phone_number} deleted successfully on production.")
        else:
            logger.warning(f"Failed to delete user {phone_number} on production. Continuing with registration.")

        tokens = self.api_auth_by_phonenumber(phone_number, confirm_code, use_prod=True)
        if not tokens:
            logger.error(f"Re-authentication failed for {phone_number} on production after deletion.")
            return

        access_token = tokens['accessToken']
        logger.info(f"New Access Token for {phone_number} on production: {access_token}")

        today = datetime.today()
        birthday = today + timedelta(days=int(days_ahead))
        birthday_str = f"1970-{birthday.strftime('%m-%d')}"

        if not self.update_user_profile(access_token, name, birthday_str, use_prod=True):
            logger.error(f"Failed to update profile for {phone_number} on production.")
            return

        if not self.update_user_contacts(access_token, phone_number, name, use_prod=True):
            logger.error(f"Failed to update contacts for {phone_number} on production.")
            return

        if not self.get_user_contacts(access_token, use_prod=True):
            logger.error(f"Failed to GET contacts for {phone_number} on production.")
            return

        logger.info(f"User {phone_number} registered and updated successfully on production.")

    def get_user_contacts(self, access_token, use_prod=False):
        """
        Fetch the user's contacts from the API.

        :param access_token: The access token of the user.
        :param use_prod: Boolean to determine if production URL should be used.
        :return: The contacts data as a list if successful, else None.
        """
        base_url = self.base_url_prod if use_prod else self.base_url
        url = f"{base_url}/v1/contacts"
        headers = self.get_headers()
        headers["Authorization"] = f"Bearer {access_token}"

        logger.debug(f"Fetching contacts for user with access token: {access_token}")
        logger.debug(f"Request Headers: {json.dumps(headers, indent=2)}")

        response = requests.get(url, headers=headers)

        logger.debug(f"Response Status Code: {response.status_code}")
        logger.debug(f"Response Body: {response.text}")

        if response.status_code == 200:
            logger.info("Contacts fetched successfully.")
            return response.json()
        else:
            logger.error(f"Error fetching contacts: {response.status_code} - {response.text}")
            return None

    def update_user_profile(self, access_token, name, birthday, use_prod=False):
        """
        Update the user's profile with the provided details.

        :param access_token: The access token of the user.
        :param name: The name of the user.
        :param birthday: The birthday date in "YYYY-MM-DD" format.
        :param use_prod: Boolean to determine if production URL should be used.
        :return: True if the profile update was successful, False otherwise.
        """
        base_url = self.base_url_prod if use_prod else self.base_url
        url = f"{base_url}/v1/profile"
        headers = self.get_headers()
        headers["Authorization"] = f"Bearer {access_token}"

        payload = {
            "name": name,
            "surname": "TestSurname",
            "birthday": birthday,
            "gender": "MALE",
            "userConfirm": True
        }

        logger.debug(f"Updating profile for user with access token: {access_token}")
        logger.debug(f"Request Payload: {json.dumps(payload, indent=2)}")
        logger.debug(f"Request Headers: {json.dumps(headers, indent=2)}")

        response = requests.put(url, json=payload, headers=headers)

        logger.debug(f"Response Status Code: {response.status_code}")
        logger.debug(f"Response Body: {response.text}")

        if response.status_code == 204:
            logger.info("Profile updated successfully.")
            return True
        else:
            logger.error(f"Error updating profile: {response.status_code} - {response.text}")
            return False

    def update_user_contacts(self, access_token, phone_number, name, use_prod=False):
        """
        Update the user's contacts with the provided details.

        :param access_token: The access token of the user.
        :param phone_number: The phone number of the user.
        :param name: The name of the user.
        :param use_prod: Boolean to determine if production URL should be used.
        :return: True if the contacts update was successful, False otherwise.
        """
        base_url = self.base_url_prod if use_prod else self.base_url
        url = f"{base_url}/v1/contacts"
        headers = self.get_headers()
        headers["Authorization"] = f"Bearer {access_token}"

        contact_payloads = {
            TestData.phone_friend1: [
                {
                    "contactId": None,
                    "userId": None,
                    "phoneNumber": "85555555555",
                    "name": "Vtoroy",
                    "isFavourite": False,
                    "showInEventFeed": False
                },
                {
                    "contactId": None,
                    "userId": None,
                    "phoneNumber": "84444444445",
                    "name": "Treti",
                    "isFavourite": False,
                    "showInEventFeed": False
                }
            ],
            TestData.phone_friend2: [
                {
                    "contactId": None,
                    "userId": None,
                    "phoneNumber": "81111111111115",
                    "name": "Firsty",
                    "isFavourite": False,
                    "showInEventFeed": False
                },
                {
                    "contactId": None,
                    "userId": None,
                    "phoneNumber": "84444444445",
                    "name": "Treti",
                    "isFavourite": False,
                    "showInEventFeed": False
                }
            ],
            TestData.phone_friend3: [
                {
                    "contactId": None,
                    "userId": None,
                    "phoneNumber": "81111111111115",
                    "name": "Firsty",
                    "isFavourite": False,
                    "showInEventFeed": False
                },
                {
                    "contactId": None,
                    "userId": None,
                    "phoneNumber": "85555555555",
                    "name": "Vtoroy",
                    "isFavourite": False,
                    "showInEventFeed": False
                }
            ]
        }

        payload = contact_payloads.get(phone_number)
        if not payload:
            logger.error(f"No contact payload defined for phone number {phone_number}")
            return False

        logger.debug(f"Updating contacts for user {name} with {phone_number}")
        logger.debug(f"Request Payload: {json.dumps(payload, indent=2)}")
        logger.debug(f"Request Headers: {json.dumps(headers, indent=2)}")

        response = requests.patch(url, json=payload, headers=headers)

        logger.debug(f"Response Status Code: {response.status_code}")
        logger.debug(f"Response Body: {response.text}")

        if response.status_code == 200:
            logger.info("Contacts updated successfully.")
            return True
        else:
            logger.error(f"Error updating contacts: {response.status_code} - {response.text}")
            return False