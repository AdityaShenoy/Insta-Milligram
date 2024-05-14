import django.test as dt

from .. import forms as f
import insta_milligram.constants as ic


class TestForm(dt.SimpleTestCase):
    def test_missing_field(self):
        form = f.UserFollowForm({})
        assert not form.is_valid()
        assert "user" in form.errors.keys()

    def test_string(self):
        form = f.UserFollowForm({"user": "test"})
        assert not form.is_valid()
        assert "user" in form.errors.keys()

    def test_valid(self):
        form = f.UserFollowForm(ic.inputs.FOLLOW_REQUEST_2)
        assert form.is_valid()
        assert len(form.errors) == 0
