import django.test as dt

import auths.views as av
import insta_milligram.tests as it


class TestUrl(dt.SimpleTestCase):
    def test_url_resolution(self):
        it.test_url_resolution("auths", av.AuthView)  # type: ignore
