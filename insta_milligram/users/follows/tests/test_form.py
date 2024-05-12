import django.test as dt

from .. import forms as f
import insta_milligram.constants as c


class TestForm(dt.SimpleTestCase):
    def test_missing_field(self):
        form = f.UserFollowForm({})
        self.assertFalse(form.is_valid())
        self.assertIn("user", form.errors.keys())

    def test_string(self):
        form = f.UserFollowForm({"user": "test"})
        self.assertFalse(form.is_valid())
        self.assertIn("user", form.errors.keys())

    def test_valid(self):
        form = f.UserFollowForm(c.inputs.FOLLOW_REQUEST_2)
        self.assertTrue(form.is_valid())
        self.assertEqual(0, len(form.errors))
