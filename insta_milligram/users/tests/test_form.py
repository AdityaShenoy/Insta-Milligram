import django.test as dt

import insta_milligram.constants.inputs as ici
import users.forms as uf


class TestForm(dt.SimpleTestCase):
    def setUp(self):
        self.signup_request = ici.signup_request(1)
        self.EMPTY_REQUEST = {k: "" for k in self.signup_request}
        self.BIG_REQUEST = {k: "a" * 51 for k in self.signup_request}
        self.SMALL_PWD_REQUEST = {**self.signup_request, **ici.SMALL_PASSWORD}

    def test_missing_field(self):
        form = uf.UserForm({})
        assert not form.is_valid()
        assert set(form.errors.keys()) == set(self.signup_request.keys())

    def test_empty(self):
        form = uf.UserForm(self.EMPTY_REQUEST)
        assert not form.is_valid()
        assert set(form.errors.keys()) == set(self.signup_request.keys())

    def test_big(self):
        form = uf.UserForm(self.BIG_REQUEST)
        assert not form.is_valid()
        assert set(form.errors.keys()) == set(self.signup_request.keys())

    def test_small_password(self):
        form = uf.UserForm(self.SMALL_PWD_REQUEST)
        assert not form.is_valid()
        assert "password" in form.errors.keys()

    def test_username_with_special_chars(self):
        form = uf.UserForm({**self.signup_request, **ici.SPECIAL_USERNAME})
        assert not form.is_valid()
        assert "username" in form.errors.keys()

    def test_valid(self):
        form = uf.UserForm(self.signup_request)
        assert form.is_valid()
        assert len(form.errors) == 0
