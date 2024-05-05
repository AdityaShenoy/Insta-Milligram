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

    def test_missing_field(self):
        response = self.client.post(du.reverse("users"))
        self.assertEqual(response.status_code, rs.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            "Invalid Data",
            response.data["message"],  # type: ignore
        )
        self.assertEqual(
            set(self.TEST_REQUEST.keys()),
            set(response.data["errors"].keys()),  # type: ignore
        )

    def test_empty(self):
        response = self.client.post(du.reverse("users"), self.EMPTY_REQUEST)
        self.assertEqual(response.status_code, rs.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            "Invalid Data",
            response.data["message"],  # type: ignore
        )
        self.assertEqual(
            set(self.TEST_REQUEST.keys()),
            set(response.data["errors"].keys()),  # type: ignore
        )

    def test_big(self):
        response = self.client.post(du.reverse("users"), self.BIG_REQUEST)
        self.assertEqual(response.status_code, rs.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            "Invalid Data",
            response.data["message"],  # type: ignore
        )
        self.assertEqual(
            set(self.TEST_REQUEST.keys()),
            set(response.data["errors"].keys()),  # type: ignore
        )

    def test_small_password(self):
        response = self.client.post(du.reverse("users"), self.SMALL_PWD_REQUEST)
        self.assertEqual(response.status_code, rs.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            "Invalid Data",
            response.data["message"],  # type: ignore
        )
        self.assertIn(
            "password",
            response.data["errors"].keys(),  # type: ignore
        )

    def test_valid(self):
        response = self.client.post(du.reverse("users"), self.TEST_REQUEST)
        self.assertEqual(response.status_code, rs.HTTP_200_OK)
        self.assertEqual("Success", response.data["message"])  # type: ignore
        user = dam.User.objects.get(username=self.TEST_REQUEST["username"])
        self.assertEqual(user.username, self.TEST_REQUEST["username"])
        self.assertTrue(user.check_password(self.TEST_REQUEST["password"]))
        self.assertEqual(user.first_name, self.TEST_REQUEST["first_name"])
        self.assertEqual(user.last_name, self.TEST_REQUEST["last_name"])
        self.assertEqual(user.email, self.TEST_REQUEST["email"])

    def test_twice(self):
        self.client.post(du.reverse("users"), self.TEST_REQUEST)
        response = self.client.post(du.reverse("users"), self.TEST_REQUEST)
        self.assertEqual(response.status_code, rs.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            "User Already Exists",
            response.data["message"],  # type: ignore
        )
