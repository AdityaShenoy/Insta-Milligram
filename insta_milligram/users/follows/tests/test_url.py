import django.test as dt

from .. import views as v
import insta_milligram.tests as t


class TestUrl(dt.SimpleTestCase):
    def test_url_resolution(self):
        t.test_url_resolution("users_followings", v.UserFollowView, [1])  # type: ignore
        t.test_url_resolution("users_followers", v.UserFollowerView, [1])  # type: ignore
