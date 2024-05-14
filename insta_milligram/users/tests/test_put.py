import django.contrib.auth.models as dcam
import django.test as dt

import rest_framework.test as rt  # type: ignore

import insta_milligram.constants as ic
import insta_milligram.tests as it


class TestView(dt.TestCase):
    def setUp(self):
        self.client = rt.APIClient()
        self.header = it.signup_and_login(
            self.client,
            ic.inputs.SIGNUP_REQUESTS[1],
        )
        it.signup_and_login(self.client, ic.inputs.SIGNUP_REQUESTS[2])

    def test_without_login(self):
        response = self.client.put(ic.urls.USERS)
        it.assert_equal_responses(response, ic.responses.TOKEN_MISSING)

    def test_without_id(self):
        response = self.client.put(
            ic.urls.USERS,
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.USER_ID_MISSING)

    def test_without_user(self):
        response = self.client.put(
            ic.urls.USERS_ID[3],
            ic.inputs.UPDATE_REQUESTS[3],
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.USER_NOT_FOUND)

    def test_update_different_user(self):
        response = self.client.put(
            ic.urls.USERS_ID[2],
            ic.inputs.UPDATE_REQUESTS[2],
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.OPERATION_NOT_ALLOWED)

    def test_invalid(self):
        response = self.client.put(
            ic.urls.USERS_ID[1],
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.INVALID_DATA)
        assert set(response.data["errors"].keys()) == set(  # type: ignore
            ic.inputs.SIGNUP_REQUEST.keys()
        )

    def test_valid(self):
        update_request = ic.inputs.UPDATE_REQUESTS[1]
        response = self.client.put(
            ic.urls.USERS_ID[1],
            update_request,
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.SUCCESS)
        user = dcam.User.objects.get(pk=1)
        for field in ic.inputs.UPDATE_REQUESTS[1]:
            if field == "password":
                continue
            assert user.__getattribute__(field) == update_request[field]
        assert user.check_password(update_request["password"])
