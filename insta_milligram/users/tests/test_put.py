import django.contrib.auth.models as dcam
import django.test as dt

import rest_framework.test as rt  # type: ignore

import insta_milligram.constants as ic
import insta_milligram.tests as it


class TestView(dt.TestCase):
    def setUp(self):
        self.client = rt.APIClient()

    def test_without_id(self):
        response = self.client.put(ic.urls.USERS)
        it.assert_equal_responses(response, ic.responses.USER_ID_MISSING)

    def test_invalid(self):
        response = self.client.put(ic.urls.USERS_ID_1)
        it.assert_equal_responses(response, ic.responses.INVALID_DATA)
        assert set(response.data["errors"].keys()) == set(  # type: ignore
            ic.inputs.SIGNUP_REQUEST.keys()
        )

    def test_valid(self):
        self.client.post(ic.urls.USERS, ic.inputs.SIGNUP_REQUEST)
        response = self.client.put(ic.urls.USERS_ID_1, ic.inputs.UPDATE_REQUEST)
        it.assert_equal_responses(response, ic.responses.SUCCESS)
        user = dcam.User.objects.get(pk=1)
        for field in ic.inputs.UPDATE_REQUEST:
            if field == "password":
                continue
            assert user.__getattribute__(field) == ic.inputs.UPDATE_REQUEST[field]
        assert user.check_password(ic.inputs.UPDATE_REQUEST["password"])

    def test_without_user(self):
        response = self.client.put(ic.urls.USERS_ID_1, ic.inputs.UPDATE_REQUEST)
        it.assert_equal_responses(response, ic.responses.USER_NOT_FOUND)
