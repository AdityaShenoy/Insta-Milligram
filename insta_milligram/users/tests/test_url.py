import django.test as dt

from .. import views as v
import insta_milligram.tests as it


class TestUrl(dt.SimpleTestCase):
    def test_url_resolution(self):
        it.test_url_resolution("users", v.UserView)  # type: ignore
        it.test_url_resolution("users_id", v.UserView, [1])  # type: ignore
