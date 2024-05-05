import django.test as dt
import django.urls as du

from .. import views as v


class TestUrl(dt.SimpleTestCase):
    def test_url_resolution(self):
        self.assertEqual(
            du.resolve(du.reverse("users")).func.cls,  # type: ignore
            v.UserView,
        )