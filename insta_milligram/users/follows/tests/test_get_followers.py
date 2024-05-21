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
        response = self.client.get(ic.urls.user_id_followers(2))
        it.assert_equal_responses(response, ic.responses.TOKEN_MISSING)

    def test_follow_wrong_user(self):
        response = self.client.get(
            ic.urls.user_id_followers(300),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.USER_NOT_FOUND)

    def test_valid(self):
        for i in range(2, 101):
            dcam.User.objects.create(**ic.inputs.signup_request(i))
        user_1 = dcam.User.objects.get(pk=1)
        for i in range(2, 101):
            user_i = dcam.User.objects.get(pk=i)
            umuf.Follow.objects.create(follower=user_i, following=user_1)

        response = self.client.get(
            ic.urls.user_id_followers(1),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.SUCCESS)

        followers = response.data["followers"]  # type: ignore
        follower_ids = {follower["id"] for follower in followers}  # type: ignore
        assert len(follower_ids) == 50  # type: ignore

        response = self.client.get(
            ic.urls.user_id_followers_page(1, 2),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.SUCCESS)

        followers = response.data["followers"]  # type: ignore
        follower_ids = {follower["id"] for follower in followers}  # type: ignore
        assert len(follower_ids) == 49  # type: ignore

        response = self.client.get(
            ic.urls.user_id_followers(2),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.SUCCESS)
        assert not response.data["followers"]  # type: ignore

    def test_invalid_page(self):
        response = self.client.get(
            ic.urls.user_id_followers_page(1, -1),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.SUCCESS)
        response = self.client.get(
            ic.urls.user_id_followers_page(1, 100),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.SUCCESS)
        response = self.client.get(
            ic.urls.user_id_followers_page(1, "a"),  # type: ignore
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.SUCCESS)
