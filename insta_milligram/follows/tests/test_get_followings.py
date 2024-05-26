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
        response = self.client.get(icu.user_id_followings(1))
        it.assert_equal_responses(response, icr.TOKEN_MISSING)

    def test_follow_wrong_user(self):
        response = self.client.get(
            icu.user_id_followings(3),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, icr.USER_NOT_FOUND)

    def test_valid(self):
        user_1 = dcam.User.objects.get(pk=1)
        for i in range(2, 101):
            profile = ump.Profile.objects.create(**ici.signup_request(i))
            user = profile.user
            fm.Follow.objects.create(follower=user_1, following=user)

        response = self.client.get(
            icu.user_id_followings(1),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, icr.SUCCESS)
        followings = response.data["followings"]  # type: ignore
        assert len(followings) == 50  # type: ignore

        response = self.client.get(
            icu.user_id_followings_page(1, 2),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, icr.SUCCESS)
        followings = response.data["followings"]  # type: ignore
        assert len(followings) == 49  # type: ignore

        response = self.client.get(
            icu.user_id_followings(2),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, icr.SUCCESS)
        followings = response.data["followings"]  # type: ignore
        assert not followings

    def test_wrong_user_id(self):
        response = self.client.get(
            icu.user_id_followings_id(1, 3),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, icr.USER_NOT_FOUND)

    def test_invalid_page(self):
        response = self.client.get(
            icu.user_id_followings_page(1, -1),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, icr.SUCCESS)
        response = self.client.get(
            icu.user_id_followings_page(1, 100),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, icr.SUCCESS)
        response = self.client.get(
            icu.user_id_followings_page(1, "a"),  # type: ignore
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, icr.SUCCESS)

    def test_valid_id(self):
        user_1 = dcam.User.objects.get(pk=1)
        user_2 = ump.Profile.objects.create(**ici.signup_request(2)).user
        fm.Follow.objects.create(follower=user_1, following=user_2)

        response = self.client.get(
            icu.user_id_followings_id(1, 2),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, icr.SUCCESS)
        assert response.data["is_following"]  # type: ignore

        response = self.client.get(
            icu.user_id_followings_id(2, 1),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, icr.SUCCESS)
        assert not response.data["is_following"]  # type: ignore
