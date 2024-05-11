import django.test as dt
import django.urls as du

import rest_framework.status as rs  # type: ignore

import insta_milligram.helpers as h
import insta_milligram.constants as c


class TestView(dt.TestCase):
    def setUp(self):
        self.USER_ID = 1

    def test_without_id(self):
        response = self.client.get(du.reverse("users"))
        h.assertEqualResponses(response, c.responses.USER_ID_MISSING)

    def test_wrong_id(self):
        response = self.client.get(du.reverse("users_id", args=[self.USER_ID]))
        h.assertEqualResponses(response, c.responses.USER_NOT_FOUND)

    def test_correct(self):
        self.client.post(du.reverse("users"), c.inputs.SIGNUP_REQUEST)
        response = self.client.get(du.reverse("users_id", args=[self.USER_ID]))
        h.assertEqualResponse(response, c.messages.SUCCESS, rs.HTTP_200_OK)
        user: dict[str, str] = response.data  # type: ignore
        for field in c.inputs.SIGNUP_REQUEST:
            if field != "password":
                self.assertEqual(user[field], c.inputs.SIGNUP_REQUEST[field])
