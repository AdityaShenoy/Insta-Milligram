import django.test as dt
import django.contrib.auth.models as dcam

import insta_milligram.constants as ic
import insta_milligram.tests as it


class TestView(dt.TestCase):
    def setUp(self):
        signup_request = ic.inputs.SIGNUP_REQUESTS[0]
        self.header = it.signup_and_login(self.client, signup_request)

    def test_without_id(self):
        response = self.client.delete(ic.urls.USERS)
        it.assert_equal_responses(response, ic.responses.USER_ID_MISSING)

    def test_without_token(self):
        response = self.client.delete(ic.urls.USERS_ID_1)
        it.assert_equal_responses(response, ic.responses.TOKEN_MISSING)
        assert len(dcam.User.objects.all()) == 1

    def test_incorrect_token(self):
        response = self.client.delete(
            ic.urls.USERS_ID_1,
            headers={"Authorization": "Bearer dummy"},  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.INVALID_TOKEN)
        assert len(dcam.User.objects.all()) == 1

    def test_expired_token(self):
        response = self.client.delete(
            ic.urls.USERS_ID_1,
            headers={  # type: ignore
                "Authorization": f"Bearer {ic.inputs.EXPIRED_ACCESS_TOKEN}",
            },
        )
        it.assert_equal_responses(response, ic.responses.INVALID_TOKEN)
        assert len(dcam.User.objects.all()) == 1

    def test_delete_twice(self):
        signup_request = ic.inputs.SIGNUP_REQUESTS[0]
        header = it.signup_and_login(self.client, signup_request)
        self.client.delete(ic.urls.USERS_ID_1, headers=header)  # type: ignore
        response = self.client.delete(
            ic.urls.USERS_ID_1,
            headers=header,  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.USER_NOT_FOUND)
