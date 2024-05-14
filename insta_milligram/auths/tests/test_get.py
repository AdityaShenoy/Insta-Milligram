import django.test as dt
import django.contrib.auth.models as dcam

import insta_milligram.constants as ic
import insta_milligram.tests as it


class TestView(dt.TestCase):
    def test_without_id(self):
        response = self.client.delete(ic.urls.USERS)
        it.assert_equal_responses(response, ic.responses.USER_ID_MISSING)

    def test_without_token(self):
        self.client.post(ic.urls.USERS, ic.inputs.SIGNUP_REQUEST)
        login_response = self.client.post(
            ic.urls.AUTHS,
            ic.inputs.LOGIN_REQUEST,
            QUERY_STRING="action=generate",
        )
        access_token = login_response.data["tokens"]["access"]  # type: ignore
        response = self.client.delete(
            ic.urls.USERS_ID_1,
        )
        it.assert_equal_responses(response, ic.responses.TOKEN_MISSING)
        assert len(dcam.User.objects.all()) == 1

    def test_incorrect_token(self):
        self.client.post(ic.urls.USERS, ic.inputs.SIGNUP_REQUEST)
        login_response = self.client.post(
            ic.urls.AUTHS,
            ic.inputs.LOGIN_REQUEST,
            QUERY_STRING="action=generate",
        )
        access_token = login_response.data["tokens"]["access"]  # type: ignore
        response = self.client.delete(
            ic.urls.USERS_ID_1,
            headers={"Authorization": f"Bearer {access_token}a"},  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.INVALID_TOKEN)
        assert len(dcam.User.objects.all()) == 1

    def test_expired_token(self):
        self.client.post(ic.urls.USERS, ic.inputs.SIGNUP_REQUEST)
        response = self.client.delete(
            ic.urls.USERS_ID_1,
            headers={"Authorization": f"Bearer {ic.inputs.EXPIRED_ACCESS_TOKEN}"},  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.INVALID_TOKEN)
        assert len(dcam.User.objects.all()) == 1

    def test_delete_twice(self):
        self.client.post(ic.urls.USERS, ic.inputs.SIGNUP_REQUEST)
        login_response = self.client.post(
            ic.urls.AUTHS,
            ic.inputs.LOGIN_REQUEST,
            QUERY_STRING="action=generate",
        )
        self.client.delete(
            ic.urls.USERS_ID_1,
            headers=it.generate_headers_old(login_response),  # type: ignore
        )
        response = self.client.delete(
            ic.urls.USERS_ID_1,
            headers=it.generate_headers_old(login_response),  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.USER_NOT_FOUND)
