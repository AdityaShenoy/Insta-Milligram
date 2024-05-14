import django.test as dt
import django.contrib.auth.models as dam

import insta_milligram.constants as c
import insta_milligram.tests as t


class TestView(dt.TestCase):
    def test_without_id(self):
        response = self.client.delete(c.urls.USERS)
        t.assert_equal_responses(response, c.responses.USER_ID_MISSING)

    def test_without_token(self):
        self.client.post(c.urls.USERS, c.inputs.SIGNUP_REQUEST)
        login_response = self.client.post(
            c.urls.AUTHS,
            c.inputs.LOGIN_REQUEST,
            QUERY_STRING="action=generate",
        )
        access_token = login_response.data["tokens"]["access"]  # type: ignore
        response = self.client.delete(
            c.urls.USERS_ID_1,
        )
        t.assert_equal_responses(response, c.responses.TOKEN_MISSING)
        assert len(dam.User.objects.all()) == 1

    def test_incorrect_token(self):
        self.client.post(c.urls.USERS, c.inputs.SIGNUP_REQUEST)
        login_response = self.client.post(
            c.urls.AUTHS,
            c.inputs.LOGIN_REQUEST,
            QUERY_STRING="action=generate",
        )
        access_token = login_response.data["tokens"]["access"]  # type: ignore
        response = self.client.delete(
            c.urls.USERS_ID_1,
            headers={"Authorization": f"Bearer {access_token}a"},  # type: ignore
        )
        t.assert_equal_responses(response, c.responses.INVALID_TOKEN)
        assert len(dam.User.objects.all()) == 1

    def test_expired_token(self):
        self.client.post(c.urls.USERS, c.inputs.SIGNUP_REQUEST)
        response = self.client.delete(
            c.urls.USERS_ID_1,
            headers={"Authorization": f"Bearer {c.inputs.EXPIRED_ACCESS_TOKEN}"},  # type: ignore
        )
        t.assert_equal_responses(response, c.responses.INVALID_TOKEN)
        assert len(dam.User.objects.all()) == 1

    def test_delete_twice(self):
        self.client.post(c.urls.USERS, c.inputs.SIGNUP_REQUEST)
        login_response = self.client.post(
            c.urls.AUTHS,
            c.inputs.LOGIN_REQUEST,
            QUERY_STRING="action=generate",
        )
        self.client.delete(
            c.urls.USERS_ID_1,
            headers=t.generate_headers(login_response),  # type: ignore
        )
        response = self.client.delete(
            c.urls.USERS_ID_1,
            headers=t.generate_headers(login_response),  # type: ignore
        )
        t.assert_equal_responses(response, c.responses.USER_NOT_FOUND)
