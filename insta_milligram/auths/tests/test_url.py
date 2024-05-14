import django.test as dt

from .. import views as v
import insta_milligram.tests as it


class TestUrl(dt.SimpleTestCase):
    def test_url_resolution(self):
        it.test_url_resolution("auths", v.AuthView)  # type: ignore
