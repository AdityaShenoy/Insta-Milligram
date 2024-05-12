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
        h.assertEqualResponse(
            response, c.messages.INVALID_DATA, rs.HTTP_400_BAD_REQUEST
        )
        self.assertIn("user", response.data["errors"])  # type: ignore

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
        self.assertEqual(user1.profile.followings_count, 1)  # type: ignore
        self.assertEqual(user2.profile.followers_count, 1)  # type: ignore
        follow = umuf.UserFollow.objects.filter(
            follower=user1,
            following=user2,
        )
        self.assertEqual(len(follow), 1)

        self.assertIn(
            user1.id,  # type: ignore
            user2.followers.all().values_list("follower", flat=True),  # type: ignore
        )
        self.assertIn(
            user2.id,  # type: ignore
            user1.followings.all().values_list("following", flat=True),  # type: ignore
        )
        # todo: convert self.assertEqual to assert statements
