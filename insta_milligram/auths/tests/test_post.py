import django.test as dt

import rest_framework.status as rs  # type: ignore

import insta_milligram.constants as c
import insta_milligram.helpers as h


class TestView(dt.TestCase):
    def test_missing_action(self):
        response = self.client.post(c.urls.AUTHS, QUERY_STRING="")
        h.assertEqualResponses(response, c.responses.INCORRECT_TOKEN_PARAMETER)

    def test_incorrect_action(self):
        response = self.client.post(c.urls.AUTHS, QUERY_STRING="action=bla")
        h.assertEqualResponses(response, c.responses.INCORRECT_TOKEN_PARAMETER)

    def test_without_login(self):
        response = self.client.post(
            c.urls.AUTHS,
            QUERY_STRING="action=generate",
        )
        h.assertEqualResponses(response, c.responses.INVALID_DATA)
        assert set(response.data["errors"].keys()) == set(  # type: ignore
            c.inputs.LOGIN_REQUEST.keys()
        )

    def test_with_login(self):
        self.client.post(c.urls.USERS, c.inputs.SIGNUP_REQUEST)
        response = self.client.post(
            c.urls.AUTHS,
            c.inputs.LOGIN_REQUEST,
            QUERY_STRING="action=generate",
        )
        h.assertEqualResponses(response, c.responses.SUCCESS)
        assert set(response.data["tokens"].keys()) == {  # type: ignore
            "access",
            "refresh",
        }

    def test_with_incorrect_user(self):
        response = self.client.post(
            c.urls.AUTHS,
            {**c.inputs.LOGIN_REQUEST, "username": "test1"},
            QUERY_STRING="action=generate",
        )
        h.assertEqualResponses(response, c.responses.INCORRECT_USER)

    def test_with_incorrect_password(self):
        self.client.post(c.urls.USERS, c.inputs.SIGNUP_REQUEST)
        response = self.client.post(
            c.urls.AUTHS,
            {**c.inputs.LOGIN_REQUEST, "password": "testpass1"},
            QUERY_STRING="action=generate",
        )
        h.assertEqualResponses(response, c.responses.INCORRECT_PASSWORD)
