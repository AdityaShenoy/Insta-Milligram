import django.test as dt

from .. import forms as f
import insta_milligram.constants as c


class TestForm(dt.SimpleTestCase):
    def setUp(self):
        self.EMPTY_REQUEST = {k: "" for k in c.inputs.SIGNUP_REQUEST}
        self.BIG_REQUEST = {k: "a" * 51 for k in c.inputs.SIGNUP_REQUEST}
        self.SMALL_PWD_REQUEST = {**c.inputs.SIGNUP_REQUEST, "password": "test"}

    def test_missing_field(self):
        form = f.UserForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            set(form.errors.keys()),
            set(c.inputs.SIGNUP_REQUEST.keys()),
        )

    def test_empty(self):
        form = f.UserForm(self.EMPTY_REQUEST)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            set(form.errors.keys()),
            set(c.inputs.SIGNUP_REQUEST.keys()),
        )

    def test_big(self):
        form = f.UserForm(self.BIG_REQUEST)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            set(form.errors.keys()),
            set(c.inputs.SIGNUP_REQUEST.keys()),
        )

    def test_small_password(self):
        form = f.UserForm(self.SMALL_PWD_REQUEST)
        self.assertFalse(form.is_valid())
        self.assertIn("password", form.errors.keys())

    def test_username_with_special_chars(self):
        form = f.UserForm({**c.inputs.SIGNUP_REQUEST, "username": "@"})
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors.keys())

    def test_valid(self):
        form = f.UserForm(c.inputs.SIGNUP_REQUEST)
        self.assertTrue(form.is_valid())
        self.assertEqual(0, len(form.errors))
