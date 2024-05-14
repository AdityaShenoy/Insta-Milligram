import django.test as dt
import django.contrib.auth.models as dam

import rest_framework.status as rs  # type: ignore
import rest_framework.test as rt  # type: ignore

import insta_milligram.constants as c
import insta_milligram.responses as r


class TestView(dt.TestCase):
    def setUp(self):
        self.client = rt.APIClient()

    def test_without_id(self):
        response = self.client.put(c.urls.USERS)
        r.assertEqualResponses(response, c.responses.USER_ID_MISSING)

    def test_invalid(self):
        response = self.client.put(c.urls.USERS_ID_1)
        r.assertEqualResponses(response, c.responses.INVALID_DATA)
        assert set(response.data["errors"].keys()) == set(  # type: ignore
            c.inputs.SIGNUP_REQUEST.keys()
        )

    def test_valid(self):
        self.client.post(c.urls.USERS, c.inputs.SIGNUP_REQUEST)
        response = self.client.put(c.urls.USERS_ID_1, c.inputs.UPDATE_REQUEST)
        r.assertEqualResponses(response, c.responses.SUCCESS)
        user = dam.User.objects.get(pk=1)
        for field in c.inputs.UPDATE_REQUEST:
            if field == "password":
                continue
            assert user.__getattribute__(field) == c.inputs.UPDATE_REQUEST[field]
        assert user.check_password(c.inputs.UPDATE_REQUEST["password"])

    def test_without_user(self):
        response = self.client.put(c.urls.USERS_ID_1, c.inputs.UPDATE_REQUEST)
        r.assertEqualResponses(response, c.responses.USER_NOT_FOUND)
