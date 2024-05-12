import django.test as dt
import django.contrib.auth.models as dam

import insta_milligram.constants as c
import insta_milligram.helpers as h


class TestView(dt.TestCase):
    def test_correct(self):
        self.client.post(c.urls.USERS, c.inputs.SIGNUP_REQUEST)
        login_response = self.client.post(
            c.urls.AUTHS,
            c.inputs.LOGIN_REQUEST,
            QUERY_STRING="action=generate",
        )
        access_token = login_response.data["tokens"]["access"]  # type: ignore
        response = self.client.delete(
            c.urls.USERS_ID_1,
            headers={"Authorization": f"Bearer {access_token}"},  # type: ignore
        )
        h.assertEqualResponses(response, c.responses.SUCCESS)
        assert len(dam.User.objects.all()) == 0

    def test_incorrect_id(self):
        self.client.post(c.urls.USERS, c.inputs.SIGNUP_REQUEST)
        self.client.post(c.urls.USERS, c.inputs.SIGNUP_REQUEST_1)
        login_response = self.client.post(
            c.urls.AUTHS,
            c.inputs.LOGIN_REQUEST,
            QUERY_STRING="action=generate",
        )
        response = self.client.delete(
            c.urls.USERS_ID_2,
            headers=h.generate_headers(login_response),  # type: ignore
        )
        h.assertEqualResponses(response, c.responses.OPERATION_NOT_ALLOWED)
        assert len(dam.User.objects.all()) == 2
