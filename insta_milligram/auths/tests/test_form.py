import django.test as dt

from .. import forms as f
import insta_milligram.constants as ic


class TestForm(dt.SimpleTestCase):
    def setUp(self):
        self.EMPTY_REQUEST = {k: "" for k in ic.inputs.LOGIN_REQUEST}
        self.BIG_REQUEST = {k: "a" * 51 for k in ic.inputs.LOGIN_REQUEST}
        self.SMALL_PWD_REQUEST = {**ic.inputs.LOGIN_REQUEST, "password": "test"}

    def test_missing_field(self):
        form = f.GenerateTokenForm({})
        assert not form.is_valid()
        assert set(form.errors.keys()) == set(ic.inputs.LOGIN_REQUEST.keys())

    def test_empty(self):
        form = f.GenerateTokenForm(self.EMPTY_REQUEST)
        assert not form.is_valid()
        assert set(form.errors.keys()) == set(ic.inputs.LOGIN_REQUEST.keys())

    def test_big(self):
        form = f.GenerateTokenForm(self.BIG_REQUEST)
        assert not form.is_valid()
        assert set(form.errors.keys()) == set(ic.inputs.LOGIN_REQUEST.keys())

    def test_small_password(self):
        form = f.GenerateTokenForm(self.SMALL_PWD_REQUEST)
        assert not form.is_valid()
        assert "password" in form.errors.keys()

    def test_username_with_special_chars(self):
        form = f.GenerateTokenForm({**ic.inputs.LOGIN_REQUEST, "username": "@"})
        assert not form.is_valid()
        assert "username" in form.errors.keys()

    def test_valid(self):
        form = f.GenerateTokenForm(ic.inputs.LOGIN_REQUEST)
        assert form.is_valid()
        assert len(form.errors) == 0
