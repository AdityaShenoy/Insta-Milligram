import django.contrib.auth.models as dcam
import django.test as dt

import datetime as d

import insta_milligram.constants as ic
import insta_milligram.tests as it
import users.models.users_follows as umuf


class TestView(dt.TestCase):
    def setUp(self):
        self.header = it.signup_and_login(
            self.client,
            ic.inputs.SIGNUP_REQUESTS[0],
        )
        it.signup_and_login(self.client, ic.inputs.SIGNUP_REQUESTS[1])

    def test_without_login(self):
        response = self.client.post(ic.urls.USERS_1_FOLLOWINGS)
        it.assert_equal_responses(response, ic.responses.TOKEN_MISSING)

    def test_invalid(self):
        response = self.client.post(
            ic.urls.USERS_1_FOLLOWINGS,
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.INVALID_DATA)
        assert "user" in response.data["errors"]  # type: ignore

    def test_self_follow(self):
        response = self.client.post(
            ic.urls.USERS_1_FOLLOWINGS,
            {"user": 1},
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.OPERATION_NOT_ALLOWED)

    def test_follow_wrong_user(self):
        response = self.client.post(
            ic.urls.USERS_1_FOLLOWINGS,
            {"user": 3},
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.USER_NOT_FOUND)

    def test_follow_twice(self):
        self.client.post(
            ic.urls.USERS_1_FOLLOWINGS,
            {"user": 2},
            headers=self.header,  # type: ignore
        )
        response = self.client.post(
            ic.urls.USERS_1_FOLLOWINGS,
            {"user": 2},
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.OPERATION_NOT_ALLOWED)

    def test_valid(self):
        response = self.client.post(
            ic.urls.USERS_1_FOLLOWINGS,
            {"user": 2},
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.SUCCESS)
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
