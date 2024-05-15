import django.test as dt

import insta_milligram.constants as ic
import users.follows.forms as uff


class TestForm(dt.SimpleTestCase):
    def test_missing_field(self):
        form = uff.UserFollowForm({})
        assert not form.is_valid()
        assert "user" in form.errors.keys()

    def test_string(self):
        form = uff.UserFollowForm({"user": "test"})
        assert not form.is_valid()
        assert "user" in form.errors.keys()

    def test_valid(self):
        form = uff.UserFollowForm(ic.inputs.FOLLOW_REQUEST_2)
        assert form.is_valid()
        assert len(form.errors) == 0
