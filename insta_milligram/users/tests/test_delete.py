import django.test as dt
import django.contrib.auth.models as dam

import rest_framework.status as rs  # type: ignore

import insta_milligram.constants as c
import insta_milligram.helpers as h


class TestView(dt.TestCase):
    def test_without_id(self):
        response = self.client.delete(c.urls.USERS)
        h.assertEqualResponses(response, c.responses.USER_ID_MISSING)

    def test_correct(self):
        self.client.post(c.urls.USERS, c.inputs.SIGNUP_REQUEST)
        login_response = self.client.post(
            c.urls.AUTHS,
            c.inputs.LOGIN_REQUEST,
            QUERY_STRING="action=generate",
        )
        access_token = login_response.data["tokens"]["access"]  # type: ignore
        response = self.client.delete(
            c.urls.USERS_ID_1,
            headers={"Authorization": f"Bearer {access_token}"},  # type: ignore
        )
        h.assertEqualResponses(response, c.responses.SUCCESS)
        self.assertEqual(len(dam.User.objects.all()), 0)

    # TODO: move verify auth logic to auths
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
        self.assertEqual(response.status_code, rs.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["message"],  # type: ignore
            "Token Missing",
        )
        self.assertEqual(len(dam.User.objects.all()), 1)

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
        self.assertEqual(response.status_code, rs.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["message"],  # type: ignore
            "Invalid Token",
        )
        self.assertEqual(len(dam.User.objects.all()), 1)

    def test_expired_token(self):
        self.client.post(c.urls.USERS, c.inputs.SIGNUP_REQUEST)
        response = self.client.delete(
            c.urls.USERS_ID_1,
            headers={"Authorization": f"Bearer {c.inputs.EXPIRED_ACCESS_TOKEN}"},  # type: ignore
        )
        self.assertEqual(response.status_code, rs.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["message"],  # type: ignore
            "Invalid Token",
        )
        self.assertEqual(len(dam.User.objects.all()), 1)

    def test_delete_twice(self):
        self.client.post(c.urls.USERS, c.inputs.SIGNUP_REQUEST)
        login_response = self.client.post(
            c.urls.AUTHS,
            c.inputs.LOGIN_REQUEST,
            QUERY_STRING="action=generate",
        )
        self.client.delete(
            c.urls.USERS_ID_1,
            headers=h.generate_headers(login_response),  # type: ignore
        )
        response = self.client.delete(
            c.urls.USERS_ID_1,
            headers=h.generate_headers(login_response),  # type: ignore
        )
        h.assertEqualResponses(response, c.responses.USER_NOT_FOUND)

    def test_incorrect_id(self):
        self.client.post(c.urls.USERS, c.inputs.SIGNUP_REQUEST)
        self.client.post(c.urls.USERS, c.inputs.SIGNUP_REQUEST_1)
        login_response = self.client.post(
            c.urls.AUTHS,
            c.inputs.LOGIN_REQUEST,
            QUERY_STRING="action=generate",
        )
        response = self.client.delete(
            c.urls.USERS_ID_2,
            headers=h.generate_headers(login_response),  # type: ignore
        )
        h.assertEqualResponses(response, c.responses.OPERATION_NOT_ALLOWED)
        self.assertEqual(len(dam.User.objects.all()), 2)
