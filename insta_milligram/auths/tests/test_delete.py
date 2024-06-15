import django.test as dt

import insta_milligram.constants.responses as icr
import insta_milligram.constants.urls as icu
import insta_milligram.tests as it


class TestView(dt.TestCase):
    def setUp(self):
        self.header = it.signup_and_login(1)
        self.header_1 = it.signup_and_login(1)
        self.header_2 = it.signup_and_login(1)

    def test_without_token(self):
        response = self.client.delete(icu.AUTHS)
        it.assert_equal_responses(response, icr.TOKEN_MISSING)

    def test_valid(self):
        response = self.client.delete(icu.AUTHS, headers=self.header)
        it.assert_equal_responses(response, icr.SUCCESS)
        response = self.client.get(icu.user_id(1), headers=self.header)
        it.assert_equal_responses(response, icr.LOGIN_BLACKLISTED)

    def test_valid_twice(self):
        response = self.client.delete(icu.AUTHS, headers=self.header_1)
        it.assert_equal_responses(response, icr.SUCCESS)
        response = self.client.get(icu.user_id(1), headers=self.header)
        it.assert_equal_responses(response, icr.LOGIN_BLACKLISTED)
        response = self.client.get(icu.user_id(1), headers=self.header_1)
        it.assert_equal_responses(response, icr.LOGIN_BLACKLISTED)
        response = self.client.get(icu.user_id(1), headers=self.header_2)
        it.assert_equal_responses(response, icr.LOGIN_BLACKLISTED)
