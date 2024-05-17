import django.test as dt

import insta_milligram.constants as ic
import insta_milligram.tests as it


class TestView(dt.TestCase):
    def setUp(self):
        self.header = it.signup_and_login(
            self.client,
            ic.inputs.signup_request(1),
        )
        it.signup_and_login(self.client, ic.inputs.signup_request(2))

        self.client.post(
            ic.urls.user_id_followings(1),
            ic.inputs.follow_request(2),
            headers=self.header,  # type: ignore
        )

    def test_without_login(self):
        response = self.client.get(ic.urls.user_id_followers(2))
        it.assert_equal_responses(response, ic.responses.TOKEN_MISSING)

    def test_follow_wrong_user(self):
        response = self.client.get(
            ic.urls.user_id_followers(3),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.USER_NOT_FOUND)

    def test_valid(self):
        response = self.client.get(
            ic.urls.user_id_followers(2),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.SUCCESS)
        assert 1 in response.data["followers"]  # type: ignore
        response = self.client.get(
            ic.urls.user_id_followers(1),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.SUCCESS)
        assert not response.data["followers"]  # type: ignore
