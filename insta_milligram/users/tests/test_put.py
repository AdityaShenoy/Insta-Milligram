import django.contrib.auth.models as dcam
import django.test as dt

import rest_framework.test as rt  # type: ignore

import insta_milligram.constants.inputs as ici
import insta_milligram.constants.responses as icr
import insta_milligram.constants.urls as icu
import insta_milligram.tests as it


class TestView(dt.TestCase):
    def setUp(self):
        self.client = rt.APIClient()
        self.header = it.signup_and_login(1)
        it.signup_and_login(2)

    def test_without_login(self):
        response = self.client.put(icu.USERS)
        it.assert_equal_responses(response, icr.TOKEN_MISSING)

    def test_without_id(self):
        response = self.client.put(icu.USERS, headers=self.header)
        it.assert_equal_responses(response, icr.USER_ID_MISSING)

    def test_without_user(self):
        response = self.client.put(
            icu.user_id(3), ici.update_request(3), headers=self.header
        )
        it.assert_equal_responses(response, icr.USER_NOT_FOUND)

    def test_update_different_user(self):
        response = self.client.put(
            icu.user_id(2), ici.update_request(2), headers=self.header
        )
        it.assert_equal_responses(response, icr.OPERATION_NOT_ALLOWED)

    def test_invalid(self):
        response = self.client.put(icu.user_id(1), headers=self.header)
        it.assert_equal_responses(response, icr.INVALID_DATA)
        assert set(response.data["errors"].keys()) == set(  # type: ignore
            ici.signup_request(1).keys()
        )

    def test_valid(self):
        update_request = ici.update_request(1)
        response = self.client.put(
            icu.user_id(1),
            update_request,
            headers=self.header,
        )
        it.assert_equal_responses(response, icr.SUCCESS)
        user = dcam.User.objects.get(pk=1)
        for field in ici.update_request(1):
            if field == "password":
                continue
            assert user.__getattribute__(field) == update_request[field]
        assert user.check_password(update_request["password"])
