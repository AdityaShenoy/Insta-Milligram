import django.contrib.auth.models as dcam
import django.test as dt

import insta_milligram.constants as ic
import insta_milligram.tests as it


class TestView(dt.TestCase):
    def setUp(self):
        self.signup_request = ic.inputs.signup_request(1)

    def test_invalid(self):
        response = self.client.post(ic.urls.USERS)
        it.assert_equal_responses(response, ic.responses.INVALID_DATA)
        assert set(response.data["errors"].keys()) == set(  # type: ignore
            ic.inputs.signup_request(1).keys()
        )

    def test_valid(self):
        response = self.client.post(ic.urls.USERS, self.signup_request)
        it.assert_equal_responses(response, ic.responses.SUCCESS)
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
        it.assert_equal_responses(response, ic.responses.USER_ALREADY_EXISTS)

    def test_twice_email(self):
        self.client.post(
            ic.urls.USERS,
            {**self.signup_request, "username": "dummy"},
        )
        response = self.client.post(ic.urls.USERS, self.signup_request)
        it.assert_equal_responses(response, ic.responses.USER_ALREADY_EXISTS)
