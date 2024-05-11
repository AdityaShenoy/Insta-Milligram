import django.test as dt
import django.urls as du
import django.contrib.auth.models as dam

import rest_framework.status as rs  # type: ignore

import insta_milligram.constants as c
import insta_milligram.helpers as h


class TestView(dt.TestCase):
    def test_invalid(self):
        response = self.client.post(du.reverse("users"))
        h.assertEqualResponse(
            response, c.messages.INVALID_DATA, rs.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            set(response.data["errors"].keys()),  # type: ignore
            set(c.inputs.SIGNUP_REQUEST.keys()),
        )

    def test_valid(self):
        response = self.client.post(
            du.reverse("users"),
            c.inputs.SIGNUP_REQUEST,
        )
        h.assertEqualResponse(response, c.messages.SUCCESS, rs.HTTP_200_OK)
        user = dam.User.objects.get(
            username=c.inputs.SIGNUP_REQUEST["username"],
        )
        self.assertEqual(user.username, c.inputs.SIGNUP_REQUEST["username"])
        self.assertTrue(
            user.check_password(c.inputs.SIGNUP_REQUEST["password"]),
        )
        self.assertEqual(user.first_name, c.inputs.SIGNUP_REQUEST["first_name"])
        self.assertEqual(user.last_name, c.inputs.SIGNUP_REQUEST["last_name"])
        self.assertEqual(user.email, c.inputs.SIGNUP_REQUEST["email"])

    def test_twice_username(self):
        self.client.post(
            du.reverse("users"),
            {
                **c.inputs.SIGNUP_REQUEST,
                "email": "test1@test.com",
            },
        )
        response = self.client.post(
            du.reverse("users"),
            c.inputs.SIGNUP_REQUEST,
        )
        h.assertEqualResponse(
            response, c.messages.USER_ALREADY_EXISTS, rs.HTTP_400_BAD_REQUEST
        )

    def test_twice_email(self):
        self.client.post(
            du.reverse("users"),
            {**c.inputs.SIGNUP_REQUEST, "username": "test1"},
        )
        response = self.client.post(
            du.reverse("users"),
            c.inputs.SIGNUP_REQUEST,
        )
        h.assertEqualResponse(
            response, c.messages.USER_ALREADY_EXISTS, rs.HTTP_400_BAD_REQUEST
        )
