import django.contrib.auth.models as dcam
import django.test as dt

import insta_milligram.constants.inputs as ici
import insta_milligram.constants.responses as icr
import insta_milligram.constants.urls as icu
import insta_milligram.tests as it


class TestView(dt.TestCase):
    def setUp(self):
        self.header = it.signup_and_login(1)

    def test_without_id(self):
        response = self.client.delete(
            icu.USERS,
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, icr.USER_ID_MISSING)

    def test_without_token(self):
        response = self.client.delete(icu.user_id(1))
        it.assert_equal_responses(response, icr.TOKEN_MISSING)
        assert len(dcam.User.objects.all()) == 1

    def test_incorrect_token(self):
        response = self.client.delete(
            icu.user_id(1),
            headers={"Authorization": "Bearer dummy"},  # type: ignore
        )
        it.assert_equal_responses(response, icr.INVALID_TOKEN)
        assert len(dcam.User.objects.all()) == 1

    def test_expired_token(self):
        response = self.client.delete(
            icu.user_id(1),
            headers={  # type: ignore
                "Authorization": f"Bearer {ici.EXPIRED_ACCESS_TOKEN}",
            },
        )
        it.assert_equal_responses(response, icr.INVALID_TOKEN)
        assert len(dcam.User.objects.all()) == 1

    def test_delete_twice(self):
        self.client.delete(
            icu.user_id(1),
            headers=self.header,  # type: ignore
        )
        response = self.client.delete(
            icu.user_id(1),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, icr.USER_NOT_FOUND)
