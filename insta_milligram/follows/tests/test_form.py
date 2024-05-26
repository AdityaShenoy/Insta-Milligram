import django.test as dt

import insta_milligram.constants.inputs as ici
import follows.forms as ff


class TestForm(dt.SimpleTestCase):
    def test_missing_field(self):
        form = ff.UserFollowForm({})
        assert not form.is_valid()
        assert "user" in form.errors.keys()

    def test_string(self):
        form = ff.UserFollowForm({"user": "test"})
        assert not form.is_valid()
        assert "user" in form.errors.keys()

    def test_valid(self):
        form = ff.UserFollowForm(ici.follow_request(2))
        assert form.is_valid()
        assert len(form.errors) == 0
