import django.contrib.auth.models as dcam
import django.test as dt

import rest_framework.test as rt  # type: ignore

import os

import insta_milligram.constants.inputs as ici
import insta_milligram.constants.responses as icr
import insta_milligram.constants.urls as icu
import insta_milligram.tests as it
import follows.models as fm


class TestView(dt.TestCase):
    def setUp(self):
        self.header = it.signup_and_login(1)
        it.signup_and_login(2)

    def test_with_login(self):
        response = self.client.get(icu.users_id_profile(1))
        it.assert_equal_responses(response, icr.TOKEN_MISSING)

    def test_wrong_id(self):
        response = self.client.get(
            icu.users_id_profile(3),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, icr.USER_NOT_FOUND)

    def test_correct(self):
        user1 = dcam.User.objects.get(pk=1)
        user2 = dcam.User.objects.get(pk=2)
        fm.Follow.objects.create(follower=user1, following=user2)
        fm.Follow.objects.create(follower=user2, following=user1)

        rt.APIClient().patch(  # type: ignore
            icu.user_id(1),
            {"profile_picture": ici.get_profile_picture(), "bio": ici.TEST_BIO},
            headers=self.header,  # type: ignore
        )

        response = self.client.get(
            icu.users_id_profile(1),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, icr.SUCCESS)
        profile = response.data["profile"]  # type: ignore
        assert profile["followings_count"] == profile["followers_count"] == 1
        assert profile["bio"] == ici.TEST_BIO
        assert profile["picture"] == ici.TEST_MEDIA_URL

        os.remove(ici.UPLOADED_PROFILE_PICTURE)
