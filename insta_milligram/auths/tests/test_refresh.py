import django.test as dt

import insta_milligram.constants.inputs as ici
import insta_milligram.constants.responses as icr
import insta_milligram.constants.urls as icu
import insta_milligram.tests as it


class TestView(dt.TestCase):
    def setUp(self):
        self.client.post(icu.USERS, ici.signup_request(1))
        response = self.client.post(
            icu.AUTHS,
            ici.signup_request(1),
            QUERY_STRING="action=generate",
        )
        self.tokens: dict[str, str] = response.data["tokens"]  # type: ignore

    def test_invalid(self):
        response = self.client.post(
            icu.AUTHS,
            QUERY_STRING="action=refresh",
        )
        it.assert_equal_responses(response, icr.INVALID_DATA)
        assert "refresh" in response.data["errors"]  # type: ignore

    def test_invalid_token(self):
        response = self.client.post(
            icu.AUTHS, ici.DUMMY_REFRESH, QUERY_STRING="action=refresh"
        )
        it.assert_equal_responses(response, icr.INVALID_TOKEN)

    def test_expired_token(self):
        response = self.client.post(
            icu.AUTHS,
            ici.EXPIRED_REFRESH_TOKEN,
            QUERY_STRING="action=refresh",
        )
        it.assert_equal_responses(response, icr.INVALID_TOKEN)

    def test_deleted_user(self):
        header = {"Authorization": f'Bearer {self.tokens["access"]}'}
        self.client.delete(icu.user_id(1), headers=header)  # type: ignore
        response = self.client.post(
            icu.AUTHS, self.tokens, QUERY_STRING="action=refresh"
        )
        it.assert_equal_responses(response, icr.USER_NOT_FOUND)

    def test_blacklisted(self):
        header = {"Authorization": f'Bearer {self.tokens["access"]}'}
        response = self.client.delete(icu.AUTHS, headers=header)  # type: ignore
        response = self.client.post(
            icu.AUTHS, self.tokens, QUERY_STRING="action=refresh"
        )
        it.assert_equal_responses(response, icr.LOGIN_BLACKLISTED)

    def test_valid(self):
        response = self.client.post(
            icu.AUTHS, self.tokens, QUERY_STRING="action=refresh"
        )
        it.assert_equal_responses(response, icr.SUCCESS)
        assert "access" in response.data  # type: ignore
