import django.test as dt

import insta_milligram.constants as ic
import insta_milligram.tests as it


class TestView(dt.TestCase):
    def test_without_id(self):
        response = self.client.get(ic.urls.USERS)
        it.assert_equal_responses(response, ic.responses.USER_ID_MISSING)

    def test_wrong_id(self):
        response = self.client.get(ic.urls.USERS_ID_1)
        it.assert_equal_responses(response, ic.responses.USER_NOT_FOUND)

    def test_correct(self):
        self.client.post(ic.urls.USERS, ic.inputs.SIGNUP_REQUEST)
        response = self.client.get(ic.urls.USERS_ID_1)
        it.assert_equal_responses(response, ic.responses.SUCCESS)
        user: dict[str, str] = response.data  # type: ignore
        for field in ic.inputs.SIGNUP_REQUEST:
            if field != "password":
                assert user[field] == ic.inputs.SIGNUP_REQUEST[field]
