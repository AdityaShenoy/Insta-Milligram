import django.test as dt

from .. import views as v
import insta_milligram.tests as t


class TestUrl(dt.SimpleTestCase):
    def test_url_resolution(self):
        t.test_url_resolution("users", v.UserView)  # type: ignore
        t.test_url_resolution("users_id", v.UserView, [1])  # type: ignore
