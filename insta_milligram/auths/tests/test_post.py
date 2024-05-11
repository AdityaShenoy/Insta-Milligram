import django.test as dt
import django.urls as du

import rest_framework.status as rs  # type: ignore

import insta_milligram.constants as c
import insta_milligram.helpers as h


class TestView(dt.TestCase):

    # TODO: make a variable for reversed urls

    def test_missing_action(self):
        response = self.client.post(du.reverse("auths"), QUERY_STRING="")
        h.assertEqualResponse(
            response,
            c.messages.INCORRECT_TOKEN_PARAMETER,
            rs.HTTP_400_BAD_REQUEST,
        )

    def test_incorrect_action(self):
        response = self.client.post(du.reverse("auths"), QUERY_STRING="action=bla")
        h.assertEqualResponse(
            response,
            c.messages.INCORRECT_TOKEN_PARAMETER,
            rs.HTTP_400_BAD_REQUEST,
        )

    def test_without_login(self):
        response = self.client.post(
            du.reverse("auths"),
            QUERY_STRING="action=generate",
        )
        h.assertEqualResponse(
            response, c.messages.INVALID_DATA, rs.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            set(response.data["errors"].keys()),  # type: ignore
            set(c.inputs.LOGIN_REQUEST.keys()),
        )

    def test_with_login(self):
        self.client.post(du.reverse("users"), c.inputs.SIGNUP_REQUEST)
        response = self.client.post(
            du.reverse("auths"),
            c.inputs.LOGIN_REQUEST,
            QUERY_STRING="action=generate",
        )
        h.assertEqualResponse(response, c.messages.SUCCESS, rs.HTTP_200_OK)
        self.assertEqual(
            set(response.data["tokens"].keys()),  # type: ignore
            {"access", "refresh"},
        )

    def test_with_incorrect_user(self):
        response = self.client.post(
            du.reverse("auths"),
            {**c.inputs.LOGIN_REQUEST, "username": "test1"},
            QUERY_STRING="action=generate",
        )
        h.assertEqualResponse(
            response, c.messages.INCORRECT_USER, rs.HTTP_401_UNAUTHORIZED
        )

    def test_with_incorrect_password(self):
        self.client.post(du.reverse("users"), c.inputs.SIGNUP_REQUEST)
        response = self.client.post(
            du.reverse("auths"),
            {**c.inputs.LOGIN_REQUEST, "password": "testpass1"},
            QUERY_STRING="action=generate",
        )
        h.assertEqualResponse(
            response, c.messages.INCORRECT_PASSWORD, rs.HTTP_401_UNAUTHORIZED
        )
