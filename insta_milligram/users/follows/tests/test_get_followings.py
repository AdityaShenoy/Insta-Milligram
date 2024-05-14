import django.test as dt

import insta_milligram.constants as ic
import insta_milligram.tests as t


class TestView(dt.TestCase):
    def setUp(self):
        self.header = t.signup_and_login(
            self.client,
            ic.inputs.SIGNUP_REQUESTS[0],
        )
        t.signup_and_login(self.client, ic.inputs.SIGNUP_REQUESTS[1])
        self.client.post(
            ic.urls.USERS_1_FOLLOWINGS,
            {"user": 2},
            headers=self.header,  # type: ignore
        )

    def test_without_login(self):
        response = self.client.get(ic.urls.USERS_1_FOLLOWINGS)
        t.assert_equal_responses(response, ic.responses.TOKEN_MISSING)

    def test_follow_wrong_user(self):
        response = self.client.get(
            ic.urls.USERS_3_FOLLOWINGS,
            headers=self.header,  # type: ignore
        )
        t.assert_equal_responses(response, ic.responses.USER_NOT_FOUND)

    def test_valid(self):
        response = self.client.get(
            ic.urls.USERS_1_FOLLOWINGS,
            headers=self.header,  # type: ignore
        )
        t.assert_equal_responses(response, ic.responses.SUCCESS)
        assert 2 in response.data["followings"]  # type: ignore

    def test_valid_id(self):
        response = self.client.get(
            ic.urls.USERS_1_FOLLOWINGS_2,
            headers=self.header,  # type: ignore
        )
        t.assert_equal_responses(response, ic.responses.SUCCESS)
        assert response.data["is_following"]  # type: ignore

    def test_wrong_user_id(self):
        response = self.client.get(
            ic.urls.USERS_1_FOLLOWINGS_3,
            headers=self.header,  # type: ignore
        )
        t.assert_equal_responses(response, ic.responses.USER_NOT_FOUND)
