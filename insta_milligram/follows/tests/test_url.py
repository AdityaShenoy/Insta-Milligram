import django.test as dt

import follows.views as fv
import insta_milligram.tests as it


class TestUrl(dt.SimpleTestCase):
    def test_url_resolution(self):
        it.test_url_resolution(
            "users_followings",
            fv.UserFollowView,  # type: ignore
            [1],
        )
        it.test_url_resolution(
            "users_followers",
            fv.UserFollowerView,  # type: ignore
            [1],
        )
