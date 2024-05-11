import django.test as dt
import django.urls as du
import django.contrib.auth.models as dam

import rest_framework.status as rs  # type: ignore
import rest_framework.test as rt  # type: ignore

import insta_milligram.constants as c
import insta_milligram.helpers as h


class TestView(dt.TestCase):
    def setUp(self):
        self.USER_ID = 1
        self.client = rt.APIClient()

    def test_without_id(self):
        response = self.client.put(du.reverse("users"))
        h.assertEqualResponses(response, c.responses.USER_ID_MISSING)

    def test_invalid(self):
        response = self.client.put(du.reverse("users_id", args=[self.USER_ID]))
        h.assertEqualResponse(
            response,
            c.messages.INVALID_DATA,
            rs.HTTP_400_BAD_REQUEST,
        )
        self.assertEqual(
            set(response.data["errors"].keys()),  # type: ignore
            set(c.inputs.SIGNUP_REQUEST.keys()),
        )

    def test_valid(self):
        self.client.post(du.reverse("users"), c.inputs.SIGNUP_REQUEST)
        response = self.client.put(
            du.reverse("users_id", args=[self.USER_ID]),
            c.inputs.UPDATE_REQUEST,
        )
        h.assertEqualResponses(response, c.responses.SUCCESS)
        user = dam.User.objects.get(pk=1)
        for field in c.inputs.UPDATE_REQUEST:
            if field != "password":
                self.assertEqual(
                    user.__getattribute__(field), c.inputs.UPDATE_REQUEST[field]
                )
        self.assertTrue(user.check_password(c.inputs.UPDATE_REQUEST["password"]))

    def test_without_user(self):
        response = self.client.put(
            du.reverse("users_id", args=[self.USER_ID]),
            c.inputs.UPDATE_REQUEST,
        )
        h.assertEqualResponses(response, c.responses.USER_NOT_FOUND)
