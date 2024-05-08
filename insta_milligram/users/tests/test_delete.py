import django.http.response as drs
import django.test as dt
import django.urls as du
import django.contrib.auth.models as dam

import rest_framework.status as rs  # type: ignore


class TestView(dt.TestCase):
    def generate_headers(self, login_response: drs.HttpResponse):
        access_token = login_response.data["tokens"]["access"]  # type: ignore
        return {"Authorization": f"Bearer {access_token}"}

    def setUp(self):
        self.TEST_REQUEST = {
            "username": "test",
            "password": "testpass",
            "email": "test@test.com",
            "first_name": "test",
            "last_name": "test",
        }
        self.TEST_REQUEST_1 = {
            "username": "test1",
            "password": "testpass1",
            "email": "test1@test.com",
            "first_name": "test1",
            "last_name": "test1",
        }
        self.LOGIN_REQUEST = {"username": "test", "password": "testpass"}
        self.USER_ID = 1
        self.INCORRECT_USER_ID = 2
        self.EXPIRED_ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE1MTQ3MzU5LCJpYXQiOjE3MTUxNDcwNTksImp0aSI6IjYxNzlkMGQ5NTk1MTQ3NTdiMGU5YTA4ZjQ2YmRiMDY5IiwidXNlcl9pZCI6MX0.0q-rm-CvDISZyR4Pksfv5Ik00ltAyV5IK2SAsHb1KaI"

    def test_without_id(self):
        response = self.client.delete(du.reverse("users"))
        self.assertEqual(response.status_code, rs.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["message"],  # type: ignore
            "User ID Missing",
        )

    def test_correct(self):
        self.client.post(du.reverse("users"), self.TEST_REQUEST)
        login_response = self.client.post(
            du.reverse("auths"),
            self.LOGIN_REQUEST,
            QUERY_STRING="action=generate",
        )
        access_token = login_response.data["tokens"]["access"]  # type: ignore
        response = self.client.delete(
            du.reverse("users_id", args=[self.USER_ID]),
            headers={"Authorization": f"Bearer {access_token}"},  # type: ignore
        )
        self.assertEqual(response.status_code, rs.HTTP_200_OK)
        self.assertEqual(
            response.data["message"],  # type: ignore
            "Success",
        )
        self.assertEqual(len(dam.User.objects.all()), 0)

    def test_without_token(self):
        self.client.post(du.reverse("users"), self.TEST_REQUEST)
        login_response = self.client.post(
            du.reverse("auths"),
            self.LOGIN_REQUEST,
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
        self.client.post(du.reverse("users"), self.TEST_REQUEST)
        login_response = self.client.post(
            du.reverse("auths"),
            self.LOGIN_REQUEST,
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
        self.client.post(du.reverse("users"), self.TEST_REQUEST)
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
        self.client.post(du.reverse("users"), self.TEST_REQUEST)
        login_response = self.client.post(
            du.reverse("auths"),
            self.LOGIN_REQUEST,
            QUERY_STRING="action=generate",
        )
        self.client.delete(
            du.reverse("users_id", args=[self.USER_ID]),
            headers=self.generate_headers(login_response),  # type: ignore
        )
        response = self.client.delete(
            du.reverse("users_id", args=[self.USER_ID]),
            headers=self.generate_headers(login_response),  # type: ignore
        )
        self.assertEqual(response.status_code, rs.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data["message"],  # type: ignore
            "User Not Found",
        )

    def test_incorrect_id(self):
        self.client.post(du.reverse("users"), self.TEST_REQUEST)
        self.client.post(du.reverse("users"), self.TEST_REQUEST_1)
        login_response = self.client.post(
            du.reverse("auths"),
            self.LOGIN_REQUEST,
            QUERY_STRING="action=generate",
        )
        response = self.client.delete(
            du.reverse("users_id", args=[self.INCORRECT_USER_ID]),
            headers=self.generate_headers(login_response),  # type: ignore
        )
        self.assertEqual(response.status_code, rs.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["message"],  # type: ignore
            "Operation Not Allowed",
        )
        self.assertEqual(len(dam.User.objects.all()), 2)
