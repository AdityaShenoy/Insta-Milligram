import django.test as dt

import users.follows.views as ufv
import insta_milligram.tests as it


class TestUrl(dt.SimpleTestCase):
    def test_url_resolution(self):
        it.test_url_resolution(
            "users_followings",
            ufv.UserFollowView,  # type: ignore
            [1],
        )
        it.test_url_resolution(
            "users_followers",
            ufv.UserFollowerView,  # type: ignore
            [1],
        )
