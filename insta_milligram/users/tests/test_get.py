import django.test as dt

import insta_milligram.constants as ic
import insta_milligram.tests as it


class TestView(dt.TestCase):
    def setUp(self):
        self.header = it.signup_and_login(
            self.client,
            ic.inputs.signup_request(1),
        )

    def test_with_login(self):
        response = self.client.get(ic.urls.USERS)
        it.assert_equal_responses(response, ic.responses.TOKEN_MISSING)

    def test_without_id(self):
        response = self.client.get(
            ic.urls.USERS,
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.USER_ID_MISSING)

    def test_wrong_id(self):
        response = self.client.get(
            ic.urls.user_id(2),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.USER_NOT_FOUND)

    def test_correct(self):
        response = self.client.get(
            ic.urls.user_id(1),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.SUCCESS)
        user: dict[str, str] = response.data  # type: ignore
        for field in ic.inputs.signup_request(1):
            if field != "password":
                assert user[field] == ic.inputs.signup_request(1)[field]
