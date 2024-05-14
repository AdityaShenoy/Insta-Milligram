import django.test as dt
import django.contrib.auth.models as dcam

import insta_milligram.constants as ic
import insta_milligram.responses as ir


class TestView(dt.TestCase):
    def setUp(self):
        self.signup_request = ic.inputs.SIGNUP_REQUESTS[0]

    def test_invalid(self):
        response = self.client.post(ic.urls.USERS)
        ir.assert_equal_responses(response, ic.responses.INVALID_DATA)
        assert set(response.data["errors"].keys()) == set(  # type: ignore
            ic.inputs.SIGNUP_REQUEST.keys()
        )

    def test_valid(self):
        response = self.client.post(ic.urls.USERS, self.signup_request)
        ir.assert_equal_responses(response, ic.responses.SUCCESS)
        user = dcam.User.objects.get(username=self.signup_request["username"])
        for field in self.signup_request:
            if field == "password":
                continue
            assert user.__getattribute__(field) == self.signup_request[field]
        assert user.check_password(self.signup_request["password"])
        assert user.profile.followers_count == 0  # type: ignore
        assert user.profile.followings_count == 0  # type: ignore

    def test_twice_username(self):
        self.client.post(
            ic.urls.USERS,
            {**self.signup_request, "email": "dummy@dummy.com"},
        )
        response = self.client.post(ic.urls.USERS, self.signup_request)
        ir.assert_equal_responses(response, ic.responses.USER_ALREADY_EXISTS)

    def test_twice_email(self):
        self.client.post(
            ic.urls.USERS,
            {**self.signup_request, "username": "dummy"},
        )
        response = self.client.post(ic.urls.USERS, self.signup_request)
        ir.assert_equal_responses(response, ic.responses.USER_ALREADY_EXISTS)
