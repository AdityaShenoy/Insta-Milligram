import django.test as dt

import rest_framework.test as rt  # type: ignore

import PIL.Image as pi

import insta_milligram.constants.inputs as ici
import insta_milligram.constants.responses as icr
import insta_milligram.constants.urls as icu
import insta_milligram.tests as it


class TestView(dt.TestCase):
    def setUp(self):
        self.client = rt.APIClient()
        self.header = it.signup_and_login(1)
        it.signup_and_login(2)

    def test_without_login(self):
        response = self.client.patch(icu.USERS)
        it.assert_equal_responses(response, icr.TOKEN_MISSING)

    def test_without_id(self):
        response = self.client.patch(
            icu.USERS,
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, icr.USER_ID_MISSING)

    def test_without_user(self):
        response = self.client.patch(
            icu.user_id(3),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, icr.USER_NOT_FOUND)

    def test_update_different_user(self):
        response = self.client.patch(
            icu.user_id(2),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, icr.OPERATION_NOT_ALLOWED)

    def test_invalid(self):
        response = self.client.patch(
            icu.user_id(1),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, icr.INVALID_USER_PATCH_DATA)

    def test_valid(self):
        response = self.client.patch(
            icu.user_id(1),
            {"profile_picture": ici.PROFILE_PICTURE},
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, icr.SUCCESS)
        img = pi.open(ici.UPLOADED_PROFILE_PICTURE)  # type: ignore
        assert img.width == img.height
        img.close()

        response = self.client.patch(
            icu.user_id(1),
            {"profile_picture": ""},
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, icr.SUCCESS)
