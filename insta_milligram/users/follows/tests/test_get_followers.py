import django.test as dt

import insta_milligram.constants as ic
import insta_milligram.tests as it


class TestView(dt.TestCase):
    def setUp(self):
        self.header = it.signup_and_login(
            self.client,
            ic.inputs.SIGNUP_REQUESTS[0],
        )
        it.signup_and_login(self.client, ic.inputs.SIGNUP_REQUESTS[1])

        self.client.post(
            ic.urls.USERS_1_FOLLOWINGS,
            {"user": 2},
            headers=self.header,  # type: ignore
        )

    def test_without_login(self):
        response = self.client.get(ic.urls.USERS_2_FOLLOWERS)
        it.assert_equal_responses(response, ic.responses.TOKEN_MISSING)

    def test_follow_wrong_user(self):
        response = self.client.get(
            ic.urls.USERS_3_FOLLOWERS,
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.USER_NOT_FOUND)

    def test_valid(self):
        response = self.client.get(
            ic.urls.USERS_2_FOLLOWERS,
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.SUCCESS)
        assert 1 in response.data["followers"]  # type: ignore
