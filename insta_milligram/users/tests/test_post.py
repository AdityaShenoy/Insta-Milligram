import django.contrib.auth.models as dcam
import django.test as dt

import insta_milligram.constants.inputs as ici
import insta_milligram.constants.responses as icr
import insta_milligram.constants.urls as icu
import insta_milligram.tests as it


class TestView(dt.TestCase):
    def test_invalid(self):
        response = self.client.post(icu.USERS)
        it.assert_equal_responses(response, icr.INVALID_DATA)
        assert set(response.data["errors"].keys()) == set(  # type: ignore
            ici.signup_request(1).keys()
        )

    def test_valid(self):
        response = self.client.post(icu.USERS, ici.signup_request(1))
        it.assert_equal_responses(response, icr.SUCCESS)
        user = dcam.User.objects.get(pk=1)
        for field in ici.signup_request(1):
            if field == "password":
                continue
            assert user.__getattribute__(field) == ici.signup_request(1)[field]
        assert user.check_password(ici.signup_request(1)["password"])
        assert user.profile.followers_count == 0  # type: ignore
        assert user.profile.followings_count == 0  # type: ignore

    def test_twice_username(self):
        self.client.post(
            icu.USERS,
            {**ici.signup_request(1), **ici.DUMMY_EMAIL},
        )
        response = self.client.post(icu.USERS, ici.signup_request(1))
        it.assert_equal_responses(response, icr.USER_ALREADY_EXISTS)

    def test_twice_email(self):
        self.client.post(
            icu.USERS,
            {**ici.signup_request(1), **ici.DUMMY_USERNAME},
        )
        response = self.client.post(icu.USERS, ici.signup_request(1))
        it.assert_equal_responses(response, icr.USER_ALREADY_EXISTS)
