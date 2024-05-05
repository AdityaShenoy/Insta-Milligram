import django.test as dt
import django.urls as du

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

    def test_without_id(self):
        with self.assertRaises(TypeError):
            self.client.get(du.reverse("users"))

    def test_wrong_id(self):
        response = self.client.get(du.reverse("users_id", args=[1]))
        self.assertEqual(response.status_code, rs.HTTP_404_NOT_FOUND)
        self.assertEqual(
            "User Not Found",
            response.data["message"],  # type: ignore
        )

    def test_correct(self):
        self.client.post(du.reverse("users"), self.TEST_REQUEST)
        response = self.client.get(du.reverse("users_id", args=[1]))
        self.assertEqual(response.status_code, rs.HTTP_200_OK)
        user: dict[str, str] = response.data  # type: ignore
        self.assertEqual(user["username"], self.TEST_REQUEST["username"])
        self.assertEqual(user["email"], self.TEST_REQUEST["email"])
        self.assertEqual(user["first_name"], self.TEST_REQUEST["first_name"])
        self.assertEqual(user["last_name"], self.TEST_REQUEST["last_name"])
