import django.test as dt
import django.contrib.auth.models as dcam

import rest_framework.status as rs  # type: ignore

import insta_milligram.constants as c
import insta_milligram.helpers as h
import users.models.users_follows as umuf


class TestView(dt.TestCase):
    def setUp(self):
        self.client.post(c.urls.USERS, c.inputs.SIGNUP_REQUEST)
        self.client.post(c.urls.USERS, c.inputs.SIGNUP_REQUEST_1)
        self.login_response = self.client.post(
            c.urls.AUTHS, c.inputs.LOGIN_REQUEST, QUERY_STRING="action=generate"
        )

    def test_without_login(self):
        response = self.client.post(c.urls.USERS_1_FOLLOWINGS)
        h.assertEqualResponses(response, c.responses.TOKEN_MISSING)

    def test_invalid(self):
        response = self.client.post(
            c.urls.USERS_1_FOLLOWINGS,
            headers=h.generate_headers(self.login_response),  # type: ignore
        )
        h.assertEqualResponses(response, c.responses.INVALID_DATA)
        assert "user" in response.data["errors"]  # type: ignore

    def test_self_follow(self):
        response = self.client.post(
            c.urls.USERS_1_FOLLOWINGS,
            {"user": 1},
            headers=h.generate_headers(self.login_response),  # type: ignore
        )
        h.assertEqualResponses(response, c.responses.OPERATION_NOT_ALLOWED)

    def test_follow_wrong_user(self):
        response = self.client.post(
            c.urls.USERS_1_FOLLOWINGS,
            {"user": 3},
            headers=h.generate_headers(self.login_response),  # type: ignore
        )
        h.assertEqualResponses(response, c.responses.USER_NOT_FOUND)

    def test_follow_twice(self):
        self.client.post(
            c.urls.USERS_1_FOLLOWINGS,
            {"user": 2},
            headers=h.generate_headers(self.login_response),  # type: ignore
        )
        response = self.client.post(
            c.urls.USERS_1_FOLLOWINGS,
            {"user": 2},
            headers=h.generate_headers(self.login_response),  # type: ignore
        )
        h.assertEqualResponses(response, c.responses.OPERATION_NOT_ALLOWED)

    def test_valid(self):
        response = self.client.post(
            c.urls.USERS_1_FOLLOWINGS,
            {"user": 2},
            headers=h.generate_headers(self.login_response),  # type: ignore
        )
        h.assertEqualResponses(response, c.responses.SUCCESS)
        user1 = dcam.User.objects.get(pk=1)
        user2 = dcam.User.objects.get(pk=2)
        assert user1.profile.followings_count == 1  # type: ignore
        assert user2.profile.followers_count == 1  # type: ignore
        assert (
            umuf.UserFollow.objects.filter(
                follower=user1,
                following=user2,
            ).exists()
        )

        assert (
            user1.id  # type: ignore
            in user2.followers.all().values_list(  # type: ignore
                "follower",
                flat=True,
            )
        )
        assert (
            user2.id  # type: ignore
            in user1.followings.all().values_list(  # type: ignore
                "following",
                flat=True,
            )
        )
