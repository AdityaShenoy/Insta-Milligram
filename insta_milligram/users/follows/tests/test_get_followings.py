import django.contrib.auth.models as dcam
import django.test as dt

import insta_milligram.constants as ic
import insta_milligram.tests as it
import users.models.follows as umuf


class TestView(dt.TestCase):
    def setUp(self):
        self.header = it.signup_and_login(
            self.client,
            ic.inputs.signup_request(1),
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
        user_1 = dcam.User.objects.get(pk=1)
        for i in range(2, 101):
            user = dcam.User.objects.create(**ic.inputs.signup_request(i))
            umuf.Follow.objects.create(follower=user_1, following=user)

        response = self.client.get(
            ic.urls.user_id_followings(1),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.SUCCESS)
        followings = response.data["followings"]  # type: ignore
        following_ids = {user["id"] for user in followings}  # type: ignore
        assert len(following_ids) == 50  # type: ignore

        response = self.client.get(
            ic.urls.user_id_followings(2),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.SUCCESS)
        followings = response.data["followings"]  # type: ignore
        assert not followings

    def test_wrong_user_id(self):
        response = self.client.get(
            ic.urls.user_id_followings_id(1, 3),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.USER_NOT_FOUND)

    def test_invalid_page(self):
        response = self.client.get(
            ic.urls.user_id_followings_page(1, -1),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.SUCCESS)
        response = self.client.get(
            ic.urls.user_id_followings_page(1, 100),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.SUCCESS)
        response = self.client.get(
            ic.urls.user_id_followings_page(1, "a"),  # type: ignore
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.SUCCESS)

    def test_valid_id(self):
        user_1 = dcam.User.objects.get(pk=1)
        user_2 = dcam.User.objects.create(**ic.inputs.signup_request(2))
        umuf.Follow.objects.create(follower=user_1, following=user_2)

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
