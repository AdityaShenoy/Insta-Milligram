import django.test as dt

import insta_milligram.constants.inputs as ici
import insta_milligram.constants.responses as icr
import insta_milligram.constants.urls as icu
import insta_milligram.tests as it


class TestView(dt.TestCase):
    def setUp(self):
        self.header = it.signup_and_login(1)

    def test_with_login(self):
        response = self.client.get(icu.USERS)
        it.assert_equal_responses(response, icr.TOKEN_MISSING)

    def test_without_id(self):
        response = self.client.get(
            icu.USERS,
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, icr.USER_ID_MISSING)

    def test_wrong_id(self):
        response = self.client.get(
            icu.user_id(2),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, icr.USER_NOT_FOUND)

    def test_correct(self):
        response = self.client.get(
            icu.user_id(1),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, icr.SUCCESS)
        user = response.data["user"]  # type: ignore
        for field in ici.signup_request(1):
            if field != "password":
                assert user[field] == ici.signup_request(1)[field]
