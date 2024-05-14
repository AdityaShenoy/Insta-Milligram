import django.test as dt

import rest_framework.status as rs  # type: ignore

import insta_milligram.responses as r
import insta_milligram.constants as c


class TestView(dt.TestCase):
    def test_without_id(self):
        response = self.client.get(c.urls.USERS)
        r.assertEqualResponses(response, c.responses.USER_ID_MISSING)

    def test_wrong_id(self):
        response = self.client.get(c.urls.USERS_ID_1)
        r.assertEqualResponses(response, c.responses.USER_NOT_FOUND)

    def test_correct(self):
        self.client.post(c.urls.USERS, c.inputs.SIGNUP_REQUEST)
        response = self.client.get(c.urls.USERS_ID_1)
        r.assertEqualResponses(response, c.responses.SUCCESS)
        user: dict[str, str] = response.data  # type: ignore
        for field in c.inputs.SIGNUP_REQUEST:
            if field != "password":
                assert user[field] == c.inputs.SIGNUP_REQUEST[field]
