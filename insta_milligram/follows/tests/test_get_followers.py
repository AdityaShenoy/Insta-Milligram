import django.contrib.auth.models as dcam
import django.test as dt

import insta_milligram.constants.inputs as ici
import insta_milligram.constants.responses as icr
import insta_milligram.constants.urls as icu
import insta_milligram.tests as it
import follows.models as fm
import users.models.profiles as ump


class TestView(dt.TestCase):
    def setUp(self):
        self.header = it.signup_and_login(1)

    def test_without_login(self):
        response = self.client.get(icu.user_id_followers(2))
        it.assert_equal_responses(response, icr.TOKEN_MISSING)

    def test_follow_wrong_user(self):
        response = self.client.get(
            icu.user_id_followers(300),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, icr.USER_NOT_FOUND)

    def test_valid(self):
        user_1 = dcam.User.objects.get(pk=1)
        for i in range(2, 101):
            profile = ump.Profile.objects.create(**ici.signup_request(i))
            user_i = profile.user
            fm.Follow.objects.create(follower=user_i, following=user_1)

        response = self.client.get(
            icu.user_id_followers(1),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, icr.SUCCESS)

        followers = response.data["followers"]  # type: ignore
        assert len(followers) == 50  # type: ignore

        response = self.client.get(
            icu.user_id_followers_page(1, 2),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, icr.SUCCESS)

        followers = response.data["followers"]  # type: ignore
        assert len(followers) == 49  # type: ignore

        response = self.client.get(
            icu.user_id_followers(2),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, icr.SUCCESS)
        assert not response.data["followers"]  # type: ignore

    def test_invalid_page(self):
        response = self.client.get(
            icu.user_id_followers_page(1, -1),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, icr.SUCCESS)
        response = self.client.get(
            icu.user_id_followers_page(1, 100),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, icr.SUCCESS)
        response = self.client.get(
            icu.user_id_followers_page(1, "a"),  # type: ignore
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, icr.SUCCESS)
