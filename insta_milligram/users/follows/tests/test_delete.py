import django.contrib.auth.models as dcam
import django.test as dt

import insta_milligram.constants as ic
import insta_milligram.tests as it
import users.models.users_follows as umuf


class TestView(dt.TestCase):
    def setUp(self):
        self.header = it.signup_and_login(
            self.client,
            ic.inputs.signup_request(1),
        )
        self.header1 = it.signup_and_login(
            self.client,
            ic.inputs.signup_request(2),
        )
        it.signup_and_login(self.client, ic.inputs.signup_request(3))
        self.client.post(
            ic.urls.user_id_followings(1),
            ic.inputs.follow_request(2),
            headers=self.header,  # type: ignore
        )

    def test_without_login(self):
        response = self.client.delete(ic.urls.user_id_followings_id(1, 2))
        it.assert_equal_responses(response, ic.responses.TOKEN_MISSING)

    def test_with_wrong_user(self):
        response = self.client.delete(
            ic.urls.user_id_followings_id(4, 2),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.USER_NOT_FOUND)
        response = self.client.delete(
            ic.urls.user_id_followings_id(2, 4),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.USER_NOT_FOUND)

    def test_with_other_user(self):
        response = self.client.delete(
            ic.urls.user_id_followings_id(2, 3),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.OPERATION_NOT_ALLOWED)

    def test_not_exists(self):
        response = self.client.delete(
            ic.urls.user_id_followings_id(2, 1),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.OPERATION_NOT_ALLOWED)

    def test_delete_twice(self):
        self.client.delete(
            ic.urls.user_id_followings_id(1, 2),
            headers=self.header,  # type: ignore
        )
        response = self.client.delete(
            ic.urls.user_id_followings_id(1, 2),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.OPERATION_NOT_ALLOWED)

    def test_valid(self):
        response = self.client.delete(
            ic.urls.user_id_followings_id(1, 2),
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.SUCCESS)
        user1 = dcam.User.objects.get(pk=1)
        user2 = dcam.User.objects.get(pk=2)
        assert user1.profile.followings_count == 0  # type: ignore
        assert user2.profile.followers_count == 0  # type: ignore
        follows = umuf.UserFollow.objects.filter(
            follower=user1,
            following=user2,
        )
        assert not follows.exists()
        assert not user2.followers.filter(  # type: ignore
            follower=user1,
        ).exists()
        assert not user1.followings.filter(  # type: ignore
            following=user2,
        ).exists()

    def test_valid_2(self):
        response = self.client.delete(
            ic.urls.user_id_followings_id(1, 2),
            headers=self.header1,  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.SUCCESS)
        user1 = dcam.User.objects.get(pk=1)
        user2 = dcam.User.objects.get(pk=2)
        assert user1.profile.followings_count == 0  # type: ignore
        assert user2.profile.followers_count == 0  # type: ignore
        follows = umuf.UserFollow.objects.filter(
            follower=user1,
            following=user2,
        )
        assert not follows.exists()
        assert not user2.followers.filter(  # type: ignore
            follower=user1,
        ).exists()
        assert not user1.followings.filter(  # type: ignore
            following=user2,
        ).exists()
