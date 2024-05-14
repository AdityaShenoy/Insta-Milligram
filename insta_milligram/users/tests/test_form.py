import django.test as dt

from .. import forms as f
import insta_milligram.constants as ic


class TestForm(dt.SimpleTestCase):
    def setUp(self):
        self.EMPTY_REQUEST = {k: "" for k in ic.inputs.SIGNUP_REQUESTS[1]}
        self.BIG_REQUEST = {k: "a" * 51 for k in ic.inputs.SIGNUP_REQUESTS[1]}
        self.SMALL_PWD_REQUEST = {
            **ic.inputs.SIGNUP_REQUESTS[1],
            "password": "test",
        }

    def test_missing_field(self):
        form = f.UserForm({})
        assert not form.is_valid()
        assert set(form.errors.keys()) == set(
            ic.inputs.SIGNUP_REQUESTS[1].keys(),
        )

    def test_empty(self):
        form = f.UserForm(self.EMPTY_REQUEST)
        assert not form.is_valid()
        assert set(form.errors.keys()) == set(
            ic.inputs.SIGNUP_REQUESTS[1].keys(),
        )

    def test_big(self):
        form = f.UserForm(self.BIG_REQUEST)
        assert not form.is_valid()
        assert set(form.errors.keys()) == set(
            ic.inputs.SIGNUP_REQUESTS[1].keys(),
        )

    def test_small_password(self):
        form = f.UserForm(self.SMALL_PWD_REQUEST)
        assert not form.is_valid()
        assert "password" in form.errors.keys()

    def test_username_with_special_chars(self):
        form = f.UserForm({**ic.inputs.SIGNUP_REQUESTS[1], "username": "@"})
        assert not form.is_valid()
        assert "username" in form.errors.keys()

    def test_valid(self):
        form = f.UserForm(ic.inputs.SIGNUP_REQUESTS[1])
        assert form.is_valid()
        assert len(form.errors) == 0
