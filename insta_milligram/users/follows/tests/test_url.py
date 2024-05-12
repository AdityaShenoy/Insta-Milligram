import django.test as dt

from .. import views as v
import insta_milligram.helpers as h


class TestUrl(dt.SimpleTestCase):
    def test_url_resolution(self):
        h.test_url_resolution("users_followings", v.UserFollowView, [1])  # type: ignore
        h.test_url_resolution("users_followers", v.UserFollowerView, [1])  # type: ignore
