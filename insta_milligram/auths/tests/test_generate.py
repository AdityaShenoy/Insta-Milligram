import django.test as dt

import insta_milligram.constants as ic
import insta_milligram.tests as it


class TestView(dt.TestCase):
    def test_missing_action(self):
        response = self.client.post(ic.urls.AUTHS, QUERY_STRING="")
        it.assert_equal_responses(
            response,
            ic.responses.INCORRECT_TOKEN_PARAMETER,
        )

    def test_incorrect_action(self):
        response = self.client.post(ic.urls.AUTHS, QUERY_STRING="action=bla")
        it.assert_equal_responses(
            response,
            ic.responses.INCORRECT_TOKEN_PARAMETER,
        )

    def test_invalid(self):
        response = self.client.post(
            ic.urls.AUTHS,
            QUERY_STRING="action=generate",
        )
        it.assert_equal_responses(response, ic.responses.INVALID_DATA)
        assert set(response.data["errors"].keys()) == (  # type: ignore
            ic.inputs.LOGIN_REQUEST_FIELDS
        )

    def test_with_login(self):
        self.client.post(ic.urls.USERS, ic.inputs.signup_request(1))
        response = self.client.post(
            ic.urls.AUTHS,
            ic.inputs.signup_request(1),
            QUERY_STRING="action=generate",
        )
        it.assert_equal_responses(response, ic.responses.SUCCESS)
        assert set(response.data["tokens"].keys()) == {  # type: ignore
            "access",
            "refresh",
        }

    def test_with_incorrect_user(self):
        response = self.client.post(
            ic.urls.AUTHS,
            {**ic.inputs.signup_request(1), "username": "test1"},
            QUERY_STRING="action=generate",
        )
        it.assert_equal_responses(response, ic.responses.INCORRECT_USER)

    def test_with_incorrect_password(self):
        self.client.post(ic.urls.USERS, ic.inputs.signup_request(1))
        response = self.client.post(
            ic.urls.AUTHS,
            {**ic.inputs.signup_request(1), "password": "testpass1"},
            QUERY_STRING="action=generate",
        )
        it.assert_equal_responses(response, ic.responses.INCORRECT_PASSWORD)
