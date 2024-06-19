import django.test as dt

import rest_framework.test as rt  # type: ignore

import PIL.Image as pi

import insta_milligram.constants.inputs as ici
import insta_milligram.constants.responses as icr
import insta_milligram.constants.urls as icu
import insta_milligram.tests as it
import users.models.profiles as ump


class TestView(dt.TestCase):
    def setUp(self):
        self.client = rt.APIClient()
        self.header = it.signup_and_login(1)
        it.signup_and_login(2)

    def test_without_login(self):
        it.test_without_login("patch", icu.USERS)

    def test_without_id(self):
        response = self.client.patch(icu.USERS, headers=self.header)
        it.assert_equal_responses(response, icr.USER_ID_MISSING)

    def test_without_user(self):
        response = self.client.patch(icu.user_id(3), headers=self.header)
        it.assert_equal_responses(response, icr.USER_NOT_FOUND)

    def test_update_different_user(self):
        response = self.client.patch(icu.user_id(2), headers=self.header)
        it.assert_equal_responses(response, icr.OPERATION_NOT_ALLOWED)

    def test_invalid(self):
        response = self.client.patch(icu.user_id(1), headers=self.header)
        it.assert_equal_responses(response, icr.INVALID_USER_PATCH_DATA)

    def test_valid(self):
        response = self.client.patch(
            icu.user_id(1),
            {"profile_picture": ici.get_profile_picture()},
            headers=self.header,
        )
        it.assert_equal_responses(response, icr.SUCCESS)

        profile = ump.Profile.objects.get(pk=1)
        assert ici.UPLOADED_PROFILE_PICTURE == profile.picture.path
        img = pi.open(ici.UPLOADED_PROFILE_PICTURE)  # type: ignore
        assert img.width == img.height
        img.close()

        response = self.client.patch(
            icu.user_id(1), {"profile_picture": ""}, headers=self.header
        )
        it.assert_equal_responses(response, icr.SUCCESS)
        profile = ump.Profile.objects.get(pk=1)
        assert not profile.picture

        response = self.client.patch(
            icu.user_id(1), {"bio": ici.TEST_BIO}, headers=self.header
        )
        it.assert_equal_responses(response, icr.SUCCESS)
        profile = ump.Profile.objects.get(pk=1)
        assert profile.bio == ici.TEST_BIO

        response = self.client.patch(
            icu.user_id(1),
            {"bio": ""},
            headers=self.header,
        )
        it.assert_equal_responses(response, icr.SUCCESS)
        profile = ump.Profile.objects.get(pk=1)
        assert not profile.bio
