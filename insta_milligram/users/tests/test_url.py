import django.test as dt

import insta_milligram.tests as it
import users.views as uv


class TestUrl(dt.SimpleTestCase):
    def test_url_resolution(self):
        it.test_url_resolution("users", uv.UserView)  # type: ignore
        it.test_url_resolution("users_id", uv.UserView, [1])  # type: ignore
