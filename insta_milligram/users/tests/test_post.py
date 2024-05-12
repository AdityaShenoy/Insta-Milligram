import django.test as dt
import django.contrib.auth.models as dam

import rest_framework.status as rs  # type: ignore

import insta_milligram.constants as c
import insta_milligram.helpers as h


class TestView(dt.TestCase):
    def test_invalid(self):
        response = self.client.post(c.urls.USERS)
        h.assertEqualResponses(response, c.responses.INVALID_DATA)
        self.assertEqual(
            set(response.data["errors"].keys()),  # type: ignore
            set(c.inputs.SIGNUP_REQUEST.keys()),
        )

    def test_valid(self):
        response = self.client.post(c.urls.USERS, c.inputs.SIGNUP_REQUEST)
        h.assertEqualResponses(response, c.responses.SUCCESS)
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
        self.assertEqual(user.profile.followers_count, 0)  # type: ignore
        self.assertEqual(user.profile.followings_count, 0)  # type: ignore

    def test_twice_username(self):
        self.client.post(
            c.urls.USERS, {**c.inputs.SIGNUP_REQUEST, "email": "test1@test.com"}
        )
        response = self.client.post(c.urls.USERS, c.inputs.SIGNUP_REQUEST)
        h.assertEqualResponses(response, c.responses.USER_ALREADY_EXISTS)

    def test_twice_email(self):
        self.client.post(
            c.urls.USERS,
            {**c.inputs.SIGNUP_REQUEST, "username": "test1"},
        )
        response = self.client.post(c.urls.USERS, c.inputs.SIGNUP_REQUEST)
        h.assertEqualResponses(response, c.responses.USER_ALREADY_EXISTS)
