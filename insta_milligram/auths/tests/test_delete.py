import django.test as dt

import insta_milligram.constants as ic
import insta_milligram.tests as it


class TestView(dt.TestCase):
    def setUp(self):
        signup_request = ic.inputs.signup_request(1)
        self.header = it.signup_and_login(self.client, signup_request)
        self.header_1 = it.signup_and_login(self.client, signup_request)
        self.header_2 = it.signup_and_login(self.client, signup_request)

    def test_without_token(self):
        response = self.client.delete(ic.urls.AUTHS)
        it.assert_equal_responses(response, ic.responses.TOKEN_MISSING)

    def test_valid(self):
        response = self.client.delete(
            ic.urls.AUTHS, headers=self.header  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.SUCCESS)
        response = self.client.get(
            ic.urls.user_id(1), headers=self.header  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.LOGIN_BLACKLISTED)

    def test_valid_twice(self):
        response = self.client.delete(
            ic.urls.AUTHS, headers=self.header_1  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.SUCCESS)
        response = self.client.get(
            ic.urls.user_id(1), headers=self.header  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.LOGIN_BLACKLISTED)
        response = self.client.get(
            ic.urls.user_id(1), headers=self.header_1  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.LOGIN_BLACKLISTED)
        response = self.client.get(
            ic.urls.user_id(1), headers=self.header_2  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.LOGIN_BLACKLISTED)
