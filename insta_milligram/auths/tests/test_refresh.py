import django.test as dt

import insta_milligram.constants as ic
import insta_milligram.tests as it


class TestView(dt.TestCase):
    def setUp(self):
        self.DUMMY_REFRESH = {"refresh": "dummy"}
        self.client.post(ic.urls.USERS, ic.inputs.signup_request(1))
        response = self.client.post(
            ic.urls.AUTHS,
            ic.inputs.signup_request(1),
            QUERY_STRING="action=generate",
        )
        self.tokens: dict[str, str] = response.data["tokens"]  # type: ignore

    def test_invalid(self):
        response = self.client.post(
            ic.urls.AUTHS,
            QUERY_STRING="action=refresh",
        )
        it.assert_equal_responses(response, ic.responses.INVALID_DATA)
        assert "refresh" in response.data["errors"]  # type: ignore

    def test_invalid_token(self):
        response = self.client.post(
            ic.urls.AUTHS, self.DUMMY_REFRESH, QUERY_STRING="action=refresh"
        )
        it.assert_equal_responses(response, ic.responses.INVALID_TOKEN)

    def test_expired_token(self):
        response = self.client.post(
            ic.urls.AUTHS,
            ic.inputs.EXPIRED_REFRESH_TOKEN,
            QUERY_STRING="action=refresh",
        )
        it.assert_equal_responses(response, ic.responses.INVALID_TOKEN)

    def test_valid(self):
        response = self.client.post(
            ic.urls.AUTHS, self.tokens, QUERY_STRING="action=refresh"
        )
        it.assert_equal_responses(response, ic.responses.SUCCESS)
        assert "access" in response.data  # type: ignore
