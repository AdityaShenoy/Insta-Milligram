import django.test as dt
import django.urls as du
import django.contrib.auth.models as dam

import rest_framework.status as rs  # type: ignore
import rest_framework.test as rt  # type: ignore


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
        self.UPDATE_REQUEST = {k: f"new_{v}" for k, v in self.TEST_REQUEST.items()}
        self.USER_ID = 1
        self.client = rt.APIClient()

    def test_without_id(self):
        response = self.client.put(du.reverse("users"))
        self.assertEqual(response.status_code, rs.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["message"],  # type: ignore
            "User ID Missing",
        )

    def test_invalid(self):
        response = self.client.put(du.reverse("users_id", args=[self.USER_ID]))
        self.assertEqual(response.status_code, rs.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            "Invalid Data",
            response.data["message"],  # type: ignore
        )
        self.assertEqual(
            set(self.TEST_REQUEST.keys()),
            set(response.data["errors"].keys()),  # type: ignore
        )

    def test_valid(self):
        self.client.post(du.reverse("users"), self.TEST_REQUEST)
        response = self.client.put(
            du.reverse("users_id", args=[self.USER_ID]),
            self.UPDATE_REQUEST,
        )
        self.assertEqual(response.status_code, rs.HTTP_200_OK)
        self.assertEqual("Success", response.data["message"])  # type: ignore
        user = dam.User.objects.get(pk=1)
        for field in self.UPDATE_REQUEST:
            if field != "password":
                self.assertEqual(
                    user.__getattribute__(field), self.UPDATE_REQUEST[field]
                )
        self.assertTrue(user.check_password(self.UPDATE_REQUEST["password"]))

    def test_without_user(self):
        response = self.client.put(
            du.reverse("users_id", args=[self.USER_ID]),
            self.UPDATE_REQUEST,
        )
        self.assertEqual(response.status_code, rs.HTTP_404_NOT_FOUND)
        self.assertEqual(
            "User Does Not Exist",
            response.data["message"],  # type: ignore
        )
