import django.test as dt
import django.urls as du
import django.contrib.auth.models as dam

import rest_framework.status as rs  # type: ignore

import insta_milligram.constants as c
import insta_milligram.helpers as h


class TestView(dt.TestCase):
    def setUp(self):
        self.USER_ID = 1
        self.INCORRECT_USER_ID = 2
        self.EXPIRED_ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE1MTQ3MzU5LCJpYXQiOjE3MTUxNDcwNTksImp0aSI6IjYxNzlkMGQ5NTk1MTQ3NTdiMGU5YTA4ZjQ2YmRiMDY5IiwidXNlcl9pZCI6MX0.0q-rm-CvDISZyR4Pksfv5Ik00ltAyV5IK2SAsHb1KaI"

    def test_without_id(self):
        response = self.client.delete(du.reverse("users"))
        h.assertEqualResponses(response, c.responses.USER_ID_MISSING)

    def test_correct(self):
        self.client.post(du.reverse("users"), c.inputs.SIGNUP_REQUEST)
        login_response = self.client.post(
            du.reverse("auths"),
            c.inputs.LOGIN_REQUEST,
            QUERY_STRING="action=generate",
        )
        access_token = login_response.data["tokens"]["access"]  # type: ignore
        response = self.client.delete(
            du.reverse("users_id", args=[self.USER_ID]),
            headers={"Authorization": f"Bearer {access_token}"},  # type: ignore
        )
        h.assertEqualResponses(response, c.responses.SUCCESS)
        self.assertEqual(len(dam.User.objects.all()), 0)

    # TODO: move verify auth logic to auths
    def test_without_token(self):
        self.client.post(du.reverse("users"), c.inputs.SIGNUP_REQUEST)
        login_response = self.client.post(
            du.reverse("auths"),
            c.inputs.LOGIN_REQUEST,
            QUERY_STRING="action=generate",
        )
        access_token = login_response.data["tokens"]["access"]  # type: ignore
        response = self.client.delete(
            du.reverse("users_id", args=[self.USER_ID]),
        )
        self.assertEqual(response.status_code, rs.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["message"],  # type: ignore
            "Token Missing",
        )
        self.assertEqual(len(dam.User.objects.all()), 1)

    def test_incorrect_token(self):
        self.client.post(du.reverse("users"), c.inputs.SIGNUP_REQUEST)
        login_response = self.client.post(
            du.reverse("auths"),
            c.inputs.LOGIN_REQUEST,
            QUERY_STRING="action=generate",
        )
        access_token = login_response.data["tokens"]["access"]  # type: ignore
        response = self.client.delete(
            du.reverse("users_id", args=[self.USER_ID]),
            headers={"Authorization": f"Bearer {access_token}a"},  # type: ignore
        )
        self.assertEqual(response.status_code, rs.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["message"],  # type: ignore
            "Invalid Token",
        )
        self.assertEqual(len(dam.User.objects.all()), 1)

    def test_expired_token(self):
        self.client.post(du.reverse("users"), c.inputs.SIGNUP_REQUEST)
        response = self.client.delete(
            du.reverse("users_id", args=[self.USER_ID]),
            headers={"Authorization": f"Bearer {self.EXPIRED_ACCESS_TOKEN}"},  # type: ignore
        )
        self.assertEqual(response.status_code, rs.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["message"],  # type: ignore
            "Invalid Token",
        )
        self.assertEqual(len(dam.User.objects.all()), 1)

    def test_delete_twice(self):
        self.client.post(du.reverse("users"), c.inputs.SIGNUP_REQUEST)
        login_response = self.client.post(
            du.reverse("auths"),
            c.inputs.LOGIN_REQUEST,
            QUERY_STRING="action=generate",
        )
        self.client.delete(
            du.reverse("users_id", args=[self.USER_ID]),
            headers=h.generate_headers(login_response),  # type: ignore
        )
        response = self.client.delete(
            du.reverse("users_id", args=[self.USER_ID]),
            headers=h.generate_headers(login_response),  # type: ignore
        )
        h.assertEqualResponses(response, c.responses.USER_NOT_FOUND)

    def test_incorrect_id(self):
        self.client.post(du.reverse("users"), c.inputs.SIGNUP_REQUEST)
        self.client.post(du.reverse("users"), c.inputs.SIGNUP_REQUEST_1)
        login_response = self.client.post(
            du.reverse("auths"),
            c.inputs.LOGIN_REQUEST,
            QUERY_STRING="action=generate",
        )
        response = self.client.delete(
            du.reverse("users_id", args=[self.INCORRECT_USER_ID]),
            headers=h.generate_headers(login_response),  # type: ignore
        )
        h.assertEqualResponses(response, c.responses.OPERATION_NOT_ALLOWED)
        self.assertEqual(len(dam.User.objects.all()), 2)
