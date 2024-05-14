import django.test as dt
import django.contrib.auth.models as dcam

import datetime as d

import insta_milligram.constants as c
import insta_milligram.responses as r
import insta_milligram.tests as t
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
        r.assert_equal_responses(response, c.responses.TOKEN_MISSING)

    def test_invalid(self):
        response = self.client.post(
            c.urls.USERS_1_FOLLOWINGS,
            headers=t.generate_headers(self.login_response),  # type: ignore
        )
        r.assert_equal_responses(response, c.responses.INVALID_DATA)
        assert "user" in response.data["errors"]  # type: ignore

    def test_self_follow(self):
        response = self.client.post(
            c.urls.USERS_1_FOLLOWINGS,
            {"user": 1},
            headers=t.generate_headers(self.login_response),  # type: ignore
        )
        r.assert_equal_responses(response, c.responses.OPERATION_NOT_ALLOWED)

    def test_follow_wrong_user(self):
        response = self.client.post(
            c.urls.USERS_1_FOLLOWINGS,
            {"user": 3},
            headers=t.generate_headers(self.login_response),  # type: ignore
        )
        r.assert_equal_responses(response, c.responses.USER_NOT_FOUND)

    def test_follow_twice(self):
        self.client.post(
            c.urls.USERS_1_FOLLOWINGS,
            {"user": 2},
            headers=t.generate_headers(self.login_response),  # type: ignore
        )
        response = self.client.post(
            c.urls.USERS_1_FOLLOWINGS,
            {"user": 2},
            headers=t.generate_headers(self.login_response),  # type: ignore
        )
        r.assert_equal_responses(response, c.responses.OPERATION_NOT_ALLOWED)

    def test_valid(self):
        response = self.client.post(
            c.urls.USERS_1_FOLLOWINGS,
            {"user": 2},
            headers=t.generate_headers(self.login_response),  # type: ignore
        )
        r.assert_equal_responses(response, c.responses.SUCCESS)
        user1 = dcam.User.objects.get(pk=1)
        user2 = dcam.User.objects.get(pk=2)
        assert user1.profile.followings_count == 1  # type: ignore
        assert user2.profile.followers_count == 1  # type: ignore
        follows = umuf.UserFollow.objects.filter(
            follower=user1,
            following=user2,
        )
        assert follows.exists()
        assert follows[0].at < d.datetime.now(tz=d.UTC)
        assert user2.followers.filter(follower=user1).exists()  # type: ignore
        assert user1.followings.filter(following=user2).exists()  # type: ignore
