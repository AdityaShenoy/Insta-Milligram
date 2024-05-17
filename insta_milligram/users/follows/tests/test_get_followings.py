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
        response = self.client.get(ic.urls.user_id_followings(1))
        it.assert_equal_responses(response, ic.responses.TOKEN_MISSING)

    def test_follow_wrong_user(self):
        response = self.client.get(
            ic.urls.user_id_followings(3),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.USER_NOT_FOUND)

    def test_valid(self):
        response = self.client.get(
            ic.urls.user_id_followings(1),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.SUCCESS)
        assert 2 in response.data["followings"]  # type: ignore

    def test_wrong_user_id(self):
        response = self.client.get(
            ic.urls.user_id_followings_id(1, 3),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.USER_NOT_FOUND)

    def test_valid_id(self):
        response = self.client.get(
            ic.urls.user_id_followings_id(1, 2),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.SUCCESS)
        assert response.data["is_following"]  # type: ignore
        response = self.client.get(
            ic.urls.user_id_followings_id(2, 1),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.SUCCESS)
        assert not response.data["is_following"]  # type: ignore
