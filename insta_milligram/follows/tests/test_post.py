import django.contrib.auth.models as dcam
import django.test as dt

import datetime as d

import insta_milligram.constants.inputs as ici
import insta_milligram.constants.responses as icr
import insta_milligram.constants.urls as icu
import insta_milligram.tests as it
import follows.models as fm


class TestView(dt.TestCase):
    def setUp(self):
        self.header = it.signup_and_login(1)
        it.signup_and_login(2)

    def test_without_login(self):
        it.test_without_login("post", icu.user_id_followings(1))

    def test_with_wrong_user(self):
        response = self.client.post(
            icu.user_id_followings(3),
            ici.follow_request(2),
            headers=self.header,
        )
        it.assert_equal_responses(response, icr.USER_NOT_FOUND)

    def test_with_other_user(self):
        response = self.client.post(
            icu.user_id_followings(2),
            ici.follow_request(1),
            headers=self.header,
        )
        it.assert_equal_responses(response, icr.OPERATION_NOT_ALLOWED)

    def test_invalid(self):
        response = self.client.post(
            icu.user_id_followings(1),
            headers=self.header,
        )
        it.assert_equal_responses(response, icr.INVALID_DATA)
        assert "user" in response.data["errors"]  # type: ignore

    def test_follow_wrong_user(self):
        response = self.client.post(
            icu.user_id_followings(1),
            ici.follow_request(3),
            headers=self.header,
        )
        it.assert_equal_responses(response, icr.USER_NOT_FOUND)

    def test_self_follow(self):
        response = self.client.post(
            icu.user_id_followings(1),
            ici.follow_request(1),
            headers=self.header,
        )
        it.assert_equal_responses(response, icr.OPERATION_NOT_ALLOWED)

    def test_follow_twice(self):
        self.client.post(
            icu.user_id_followings(1),
            ici.follow_request(2),
            headers=self.header,
        )
        response = self.client.post(
            icu.user_id_followings(1),
            ici.follow_request(2),
            headers=self.header,
        )
        it.assert_equal_responses(response, icr.OPERATION_NOT_ALLOWED)

    def test_valid(self):
        response = self.client.post(
            icu.user_id_followings(1),
            ici.follow_request(2),
            headers=self.header,
        )
        it.assert_equal_responses(response, icr.SUCCESS)
        user1 = dcam.User.objects.get(pk=1)
        user2 = dcam.User.objects.get(pk=2)
        assert user1.profile.followings_count == 1  # type: ignore
        assert user2.profile.followers_count == 1  # type: ignore
        follows = fm.Follow.objects.filter(follower=user1, following=user2)
        assert follows.exists()
        assert follows[0].at < d.datetime.now(tz=d.UTC)
        assert user2.followers.filter(follower=user1).exists()  # type: ignore
        assert user1.followings.filter(following=user2).exists()  # type: ignore
