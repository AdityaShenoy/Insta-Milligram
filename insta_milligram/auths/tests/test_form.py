import django.test as dt

import auths.forms as af
import insta_milligram.constants.inputs as ici


class TestForm(dt.SimpleTestCase):
    def setUp(self):
        self.EMPTY_REQUEST = {k: "" for k in ici.signup_request(1)}
        self.BIG_REQUEST = {k: "a" * 51 for k in ici.signup_request(1)}
        self.SMALL_PWD_REQUEST = {
            **ici.signup_request(1),
            "password": "test",
        }

    def test_missing_field(self):
        form = af.GenerateTokenForm({})
        assert not form.is_valid()
        assert set(form.errors.keys()) == ici.LOGIN_REQUEST_FIELDS

        form = af.RefreshTokenForm({})
        assert not form.is_valid()
        assert "refresh" in form.errors

    def test_empty(self):
        form = af.GenerateTokenForm(self.EMPTY_REQUEST)
        assert not form.is_valid()
        assert set(form.errors.keys()) == ici.LOGIN_REQUEST_FIELDS

        form = af.RefreshTokenForm({"refresh": ""})
        assert not form.is_valid()
        assert "refresh" in form.errors

    def test_big(self):
        form = af.GenerateTokenForm(self.BIG_REQUEST)
        assert not form.is_valid()
        assert set(form.errors.keys()) == ici.LOGIN_REQUEST_FIELDS

    def test_small_password(self):
        form = af.GenerateTokenForm(self.SMALL_PWD_REQUEST)
        assert not form.is_valid()
        assert "password" in form.errors.keys()

    def test_username_with_special_chars(self):
        form = af.GenerateTokenForm(
            {**ici.signup_request(1), "username": "@"},
        )
        assert not form.is_valid()
        assert "username" in form.errors.keys()

    def test_valid(self):
        form = af.GenerateTokenForm(ici.signup_request(1))
        assert form.is_valid()
        assert len(form.errors) == 0
