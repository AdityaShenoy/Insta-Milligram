import django.test as dt

from .. import views as v
import insta_milligram.tests as t


class TestUrl(dt.SimpleTestCase):
    def test_url_resolution(self):
        t.test_url_resolution("auths", v.AuthView)  # type: ignore
