import django.test as dt
import django.urls as du
import django.contrib.auth.models as dam

import rest_framework.status as rs  # type: ignore


class TestView(dt.TestCase):
    def setUp(self):
        self.TEST_REQUEST = {
            "username": "test",
            "password": "testpass",
            "email": "test@test.com",
            "first_name": "test",
            "last_name": "test",
        }
        self.EMPTY_REQUEST = {k: "" for k in self.TEST_REQUEST}
        self.BIG_REQUEST = {k: "a" * 51 for k in self.TEST_REQUEST}
        self.SMALL_PWD_REQUEST = {**self.TEST_REQUEST, "password": "test"}

    def test_invalid(self):
        response = self.client.post(du.reverse("users"))
        self.assertEqual(response.status_code, rs.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["message"],  # type: ignore
            "Invalid Data",
        )
        self.assertEqual(
            set(response.data["errors"].keys()),  # type: ignore
            set(self.TEST_REQUEST.keys()),
        )

    def test_valid(self):
        response = self.client.post(du.reverse("users"), self.TEST_REQUEST)
        self.assertEqual(response.status_code, rs.HTTP_200_OK)
        self.assertEqual(
            response.data["message"],  # type: ignore
            "Success",
        )
        user = dam.User.objects.get(username=self.TEST_REQUEST["username"])
        self.assertEqual(user.username, self.TEST_REQUEST["username"])
        self.assertTrue(user.check_password(self.TEST_REQUEST["password"]))
        self.assertEqual(user.first_name, self.TEST_REQUEST["first_name"])
        self.assertEqual(user.last_name, self.TEST_REQUEST["last_name"])
        self.assertEqual(user.email, self.TEST_REQUEST["email"])

    def test_twice_username(self):
        self.client.post(
            du.reverse("users"), {**self.TEST_REQUEST, "email": "test1@test.com"}
        )
        response = self.client.post(du.reverse("users"), self.TEST_REQUEST)
        self.assertEqual(response.status_code, rs.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["message"],  # type: ignore
            "User Already Exists",
        )

    def test_twice_email(self):
        self.client.post(
            du.reverse("users"), {**self.TEST_REQUEST, "username": "test1"}
        )
        response = self.client.post(du.reverse("users"), self.TEST_REQUEST)
        self.assertEqual(response.status_code, rs.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["message"],  # type: ignore
            "User Already Exists",
        )
