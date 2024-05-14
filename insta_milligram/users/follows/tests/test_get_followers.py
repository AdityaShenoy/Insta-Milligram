import django.test as dt

import insta_milligram.constants as c
import insta_milligram.tests as t


class TestView(dt.TestCase):
    def setUp(self):
        self.header = t.signup_and_login(
            self.client,
            c.inputs.SIGNUP_REQUESTS[0],
        )
        t.signup_and_login(self.client, c.inputs.SIGNUP_REQUESTS[1])

        self.client.post(
            c.urls.USERS_1_FOLLOWINGS,
            {"user": 2},
            headers=self.header,  # type: ignore
        )

    def test_without_login(self):
        response = self.client.get(c.urls.USERS_2_FOLLOWERS)
        t.assert_equal_responses(response, c.responses.TOKEN_MISSING)

    def test_follow_wrong_user(self):
        response = self.client.get(
            c.urls.USERS_3_FOLLOWERS,
            headers=self.header,  # type: ignore
        )
        t.assert_equal_responses(response, c.responses.USER_NOT_FOUND)

    def test_valid(self):
        response = self.client.get(
            c.urls.USERS_2_FOLLOWERS,
            headers=self.header,  # type: ignore
        )
        t.assert_equal_responses(response, c.responses.SUCCESS)
        assert 1 in response.data["followers"]  # type: ignore
