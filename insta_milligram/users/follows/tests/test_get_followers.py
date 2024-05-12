import django.test as dt

import insta_milligram.constants as c
import insta_milligram.helpers as h


class TestView(dt.TestCase):
    def setUp(self):
        self.client.post(c.urls.USERS, c.inputs.SIGNUP_REQUEST)
        self.client.post(c.urls.USERS, c.inputs.SIGNUP_REQUEST_1)
        self.login_response = self.client.post(
            c.urls.AUTHS, c.inputs.LOGIN_REQUEST, QUERY_STRING="action=generate"
        )
        self.client.post(
            c.urls.USERS_1_FOLLOWINGS,
            {"user": 2},
            headers=h.generate_headers(self.login_response),  # type: ignore
        )

    def test_without_login(self):
        response = self.client.get(c.urls.USERS_2_FOLLOWERS)
        h.assertEqualResponses(response, c.responses.TOKEN_MISSING)

    def test_follow_wrong_user(self):
        response = self.client.get(
            c.urls.USERS_3_FOLLOWERS,
            headers=h.generate_headers(self.login_response),  # type: ignore
        )
        h.assertEqualResponses(response, c.responses.USER_NOT_FOUND)

    def test_valid(self):
        response = self.client.get(
            c.urls.USERS_2_FOLLOWERS,
            headers=h.generate_headers(self.login_response),  # type: ignore
        )
        h.assertEqualResponses(response, c.responses.SUCCESS)
        assert 1 in response.data["followers"]  # type: ignore
