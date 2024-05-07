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
        self.USER_ID = 1

    def test_without_id(self):
        response = self.client.get(du.reverse("users"))
        self.assertEqual(response.status_code, rs.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["message"],  # type: ignore
            "User ID Missing",
        )

    def test_wrong_id(self):
        response = self.client.get(du.reverse("users_id", args=[self.USER_ID]))
        self.assertEqual(response.status_code, rs.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data["message"],  # type: ignore
            "User Not Found",
        )

    def test_correct(self):
        self.client.post(du.reverse("users"), self.TEST_REQUEST)
        response = self.client.get(du.reverse("users_id", args=[self.USER_ID]))
        self.assertEqual(response.status_code, rs.HTTP_200_OK)
        user: dict[str, str] = response.data  # type: ignore
        for field in self.TEST_REQUEST:
            if field != "password":
                self.assertEqual(user[field], self.TEST_REQUEST[field])
