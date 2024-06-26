import django.contrib.auth.models as dcam
import django.test as dt

import insta_milligram.constants.inputs as ici
import insta_milligram.constants.responses as icr
import insta_milligram.constants.urls as icu
import insta_milligram.tests as it
import follows.models as fm


class TestView(dt.TestCase):
    def setUp(self):
        self.header = it.signup_and_login(1)
        self.header1 = it.signup_and_login(2)
        it.signup_and_login(3)
        self.client.post(
            icu.user_id_followings(1),
            ici.follow_request(2),
            headers=self.header,
        )

    def test_without_login(self):
        it.test_without_login("delete", icu.user_id_followings_id(1, 2))

    def test_with_wrong_user(self):
        response = self.client.delete(
            icu.user_id_followings_id(4, 2), headers=self.header
        )
        it.assert_equal_responses(response, icr.USER_NOT_FOUND)
        response = self.client.delete(
            icu.user_id_followings_id(2, 4), headers=self.header
        )
        it.assert_equal_responses(response, icr.USER_NOT_FOUND)

    def test_with_other_user(self):
        response = self.client.delete(
            icu.user_id_followings_id(2, 3), headers=self.header
        )
        it.assert_equal_responses(response, icr.OPERATION_NOT_ALLOWED)

    def test_not_exists(self):
        response = self.client.delete(
            icu.user_id_followings_id(2, 1), headers=self.header
        )
        it.assert_equal_responses(response, icr.OPERATION_NOT_ALLOWED)

    def test_valid(self):
        response = self.client.delete(
            icu.user_id_followings_id(1, 2), headers=self.header
        )
        it.assert_equal_responses(response, icr.SUCCESS)
        user1 = dcam.User.objects.get(pk=1)
        user2 = dcam.User.objects.get(pk=2)
        assert user1.profile.followings_count == 0  # type: ignore
        assert user2.profile.followers_count == 0  # type: ignore
        follows = fm.Follow.objects.filter(follower=user1, following=user2)
        assert not follows.exists()
        assert not user2.followers.filter(  # type: ignore
            follower=user1,
        ).exists()
        assert not user1.followings.filter(  # type: ignore
            following=user2,
        ).exists()

        self.client.post(
            icu.user_id_followings(1),
            ici.follow_request(2),
            headers=self.header,
        )
        response = self.client.delete(
            icu.user_id_followings_id(1, 2), headers=self.header1
        )
        it.assert_equal_responses(response, icr.SUCCESS)
        user1 = dcam.User.objects.get(pk=1)
        user2 = dcam.User.objects.get(pk=2)
        assert user1.profile.followings_count == 0  # type: ignore
        assert user2.profile.followers_count == 0  # type: ignore
        follows = fm.Follow.objects.filter(follower=user1, following=user2)
        assert not follows.exists()
        assert not user2.followers.filter(  # type: ignore
            follower=user1,
        ).exists()
        assert not user1.followings.filter(  # type: ignore
            following=user2,
        ).exists()

    def test_delete_follower_user(self):
        user1 = dcam.User.objects.get(pk=1)
        user2 = dcam.User.objects.get(pk=2)

        user1.profile.delete()  # type: ignore
        assert user2.profile.followers_count == 0  # type: ignore

    def test_delete_following_user(self):
        user1 = dcam.User.objects.get(pk=1)
        user2 = dcam.User.objects.get(pk=2)

        user2.profile.delete()  # type: ignore
        assert user1.profile.followings_count == 0  # type: ignore
