import django.test as dt
import django.urls as du

import rest_framework.status as rs  # type: ignore


class TestView(dt.TestCase):
    def setUp(self):
        self.SIGNUP_REQUEST = {
            "username": "test",
            "password": "testpass",
            "email": "test@test.com",
            "first_name": "test",
            "last_name": "test",
        }
        self.LOGIN_REQUEST = {"username": "test", "password": "testpass"}
        self.TOKEN_FIELDS = {"access", "refresh"}

    def test_missing_action(self):
        response = self.client.post(du.reverse("auths"), QUERY_STRING="")
        self.assertEqual(response.status_code, rs.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["message"],  # type: ignore
            "Incorrect Parameter - Expected ?action=generate or ?action=refresh",
        )

    def test_incorrect_action(self):
        response = self.client.post(du.reverse("auths"), QUERY_STRING="action=bla")
        self.assertEqual(response.status_code, rs.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["message"],  # type: ignore
            "Incorrect Parameter - Expected ?action=generate or ?action=refresh",
        )

    def test_without_login(self):
        response = self.client.post(
            du.reverse("auths"),
            QUERY_STRING="action=generate",
        )
        self.assertEqual(response.status_code, rs.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["message"],  # type: ignore
            "Invalid Data",
        )
        self.assertEqual(
            set(response.data["errors"].keys()),  # type: ignore
            set(self.LOGIN_REQUEST.keys()),
        )

    def test_with_login(self):
        self.client.post(du.reverse("users"), self.SIGNUP_REQUEST)
        response = self.client.post(
            du.reverse("auths"),
            self.LOGIN_REQUEST,
            QUERY_STRING="action=generate",
        )
        self.assertEqual(response.status_code, rs.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Success")  # type: ignore
        self.assertEqual(
            set(response.data["tokens"].keys()), self.TOKEN_FIELDS  # type: ignore
        )

    def test_with_incorrect_user(self):
        response = self.client.post(
            du.reverse("auths"),
            {**self.LOGIN_REQUEST, "username": "test1"},
            QUERY_STRING="action=generate",
        )
        self.assertEqual(response.status_code, rs.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["message"],  # type: ignore
            "User Not Found",
        )

    def test_with_incorrect_password(self):
        self.client.post(du.reverse("users"), self.SIGNUP_REQUEST)
        response = self.client.post(
            du.reverse("auths"),
            {**self.LOGIN_REQUEST, "password": "testpass1"},
            QUERY_STRING="action=generate",
        )
        self.assertEqual(response.status_code, rs.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["message"],  # type: ignore
            "Incorrect Password",
        )
