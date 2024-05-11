import django.test as dt

from .. import forms as f
import insta_milligram.constants as c


class TestForm(dt.SimpleTestCase):
    def setUp(self):
        self.EMPTY_REQUEST = {k: "" for k in c.inputs.LOGIN_REQUEST}
        self.BIG_REQUEST = {k: "a" * 51 for k in c.inputs.LOGIN_REQUEST}
        self.SMALL_PWD_REQUEST = {**c.inputs.LOGIN_REQUEST, "password": "test"}

    def test_missing_field(self):
        form = f.GenerateTokenForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            set(form.errors.keys()),
            set(c.inputs.LOGIN_REQUEST.keys()),
        )

    def test_empty(self):
        form = f.GenerateTokenForm(self.EMPTY_REQUEST)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            set(form.errors.keys()),
            set(c.inputs.LOGIN_REQUEST.keys()),
        )

    def test_big(self):
        form = f.GenerateTokenForm(self.BIG_REQUEST)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            set(form.errors.keys()),
            set(c.inputs.LOGIN_REQUEST.keys()),
        )

    def test_small_password(self):
        form = f.GenerateTokenForm(self.SMALL_PWD_REQUEST)
        self.assertFalse(form.is_valid())
        self.assertIn("password", form.errors.keys())

    def test_username_with_special_chars(self):
        form = f.GenerateTokenForm({**c.inputs.LOGIN_REQUEST, "username": "@"})
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors.keys())

    def test_valid(self):
        form = f.GenerateTokenForm(c.inputs.LOGIN_REQUEST)
        self.assertTrue(form.is_valid())
        self.assertEqual(0, len(form.errors))
