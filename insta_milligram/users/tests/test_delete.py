import django.contrib.auth.models as dcam
import django.test as dt

import insta_milligram.constants.responses as icr
import insta_milligram.constants.urls as icu
import insta_milligram.tests as it


class TestView(dt.TestCase):
    def setUp(self):
        self.header = it.signup_and_login(1)
        it.signup_and_login(2)

    def test_without_login(self):
        response = self.client.delete(icu.user_id(1))
        it.assert_equal_responses(response, icr.TOKEN_MISSING)

    def test_without_id(self):
        response = self.client.delete(
            icu.USERS,
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, icr.USER_ID_MISSING)

    def test_incorrect_id(self):
        response = self.client.delete(
            icu.user_id(3),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, icr.USER_NOT_FOUND)
        assert len(dcam.User.objects.all()) == 2

    def test_delete_other_user(self):
        response = self.client.delete(
            icu.user_id(2),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, icr.OPERATION_NOT_ALLOWED)
        assert len(dcam.User.objects.all()) == 2

    def test_correct(self):
        response = self.client.delete(
            icu.user_id(1),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, icr.SUCCESS)
        assert len(dcam.User.objects.all()) == 1
