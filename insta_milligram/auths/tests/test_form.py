import django.test as dt

from .. import forms as f
import insta_milligram.constants as ic


class TestForm(dt.SimpleTestCase):
    def setUp(self):
        self.EMPTY_REQUEST = {k: "" for k in ic.inputs.signup_request(1)}
        self.BIG_REQUEST = {k: "a" * 51 for k in ic.inputs.signup_request(1)}
        self.SMALL_PWD_REQUEST = {
            **ic.inputs.signup_request(1),
            "password": "test",
        }

    def test_missing_field(self):
        form = f.GenerateTokenForm({})
        assert not form.is_valid()
        assert set(form.errors.keys()) == ic.inputs.LOGIN_REQUEST_FIELDS

        form = f.RefreshTokenForm({})
        assert not form.is_valid()
        assert "refresh" in form.errors

    def test_empty(self):
        form = f.GenerateTokenForm(self.EMPTY_REQUEST)
        assert not form.is_valid()
        assert set(form.errors.keys()) == ic.inputs.LOGIN_REQUEST_FIELDS

        form = f.RefreshTokenForm({"refresh": ""})
        assert not form.is_valid()
        assert "refresh" in form.errors

    def test_big(self):
        form = f.GenerateTokenForm(self.BIG_REQUEST)
        assert not form.is_valid()
        assert set(form.errors.keys()) == ic.inputs.LOGIN_REQUEST_FIELDS

    def test_small_password(self):
        form = f.GenerateTokenForm(self.SMALL_PWD_REQUEST)
        assert not form.is_valid()
        assert "password" in form.errors.keys()

    def test_username_with_special_chars(self):
        form = f.GenerateTokenForm(
            {**ic.inputs.signup_request(1), "username": "@"},
        )
        assert not form.is_valid()
        assert "username" in form.errors.keys()

    def test_valid(self):
        form = f.GenerateTokenForm(ic.inputs.signup_request(1))
        assert form.is_valid()
        assert len(form.errors) == 0
