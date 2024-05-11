import django.test as dt

from .. import views as v
import insta_milligram.helpers as h


class TestUrl(dt.SimpleTestCase):
    def test_url_resolution(self):
        h.test_url_resolution("auths", v.AuthView)  # type: ignore
