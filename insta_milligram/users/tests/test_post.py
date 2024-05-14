import django.test as dt
import django.contrib.auth.models as dcam

import insta_milligram.constants as ic
import insta_milligram.responses as ir


class TestView(dt.TestCase):
    def test_invalid(self):
        response = self.client.post(ic.urls.USERS)
        ir.assert_equal_responses(response, ic.responses.INVALID_DATA)
        assert set(response.data["errors"].keys()) == set(  # type: ignore
            ic.inputs.SIGNUP_REQUEST.keys()
        )

    def test_valid(self):
        response = self.client.post(ic.urls.USERS, ic.inputs.SIGNUP_REQUEST)
        ir.assert_equal_responses(response, ic.responses.SUCCESS)
        user = dcam.User.objects.get(
            username=ic.inputs.SIGNUP_REQUEST["username"],
        )
        assert user.username == ic.inputs.SIGNUP_REQUEST["username"]
        assert user.check_password(ic.inputs.SIGNUP_REQUEST["password"])
        assert user.first_name == ic.inputs.SIGNUP_REQUEST["first_name"]
        assert user.last_name == ic.inputs.SIGNUP_REQUEST["last_name"]
        assert user.email == ic.inputs.SIGNUP_REQUEST["email"]
        assert user.profile.followers_count == 0  # type: ignore
        assert user.profile.followings_count == 0  # type: ignore

    def test_twice_username(self):
        self.client.post(
            ic.urls.USERS, {**ic.inputs.SIGNUP_REQUEST, "email": "test1@test.com"}
        )
        response = self.client.post(ic.urls.USERS, ic.inputs.SIGNUP_REQUEST)
        ir.assert_equal_responses(response, ic.responses.USER_ALREADY_EXISTS)

    def test_twice_email(self):
        self.client.post(
            ic.urls.USERS,
            {**ic.inputs.SIGNUP_REQUEST, "username": "test1"},
        )
        response = self.client.post(ic.urls.USERS, ic.inputs.SIGNUP_REQUEST)
        ir.assert_equal_responses(response, ic.responses.USER_ALREADY_EXISTS)
