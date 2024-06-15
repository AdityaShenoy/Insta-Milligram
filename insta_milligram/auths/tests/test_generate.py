import django.test as dt

import insta_milligram.constants.inputs as ici
import insta_milligram.constants.responses as icr
import insta_milligram.constants.urls as icu
import insta_milligram.tests as it


class TestView(dt.TestCase):
    def test_missing_action(self):
        response = self.client.post(icu.AUTHS, QUERY_STRING="")
        it.assert_equal_responses(
            response,
            icr.INCORRECT_TOKEN_PARAMETER,
        )

    def test_incorrect_action(self):
        response = self.client.post(icu.AUTHS, QUERY_STRING="action=bla")
        it.assert_equal_responses(
            response,
            icr.INCORRECT_TOKEN_PARAMETER,
        )

    def test_invalid(self):
        response = self.client.post(
            icu.AUTHS,
            QUERY_STRING="action=generate",
        )
        it.assert_equal_responses(response, icr.INVALID_DATA)
        assert set(response.data["errors"].keys()) == (  # type: ignore
            ici.LOGIN_REQUEST_FIELDS
        )

    def test_valid(self):
        self.client.post(icu.USERS, ici.signup_request(1))
        response = self.client.post(
            icu.AUTHS,
            ici.signup_request(1),
            QUERY_STRING="action=generate",
        )
        it.assert_equal_responses(response, icr.SUCCESS)
        assert set(response.data["tokens"].keys()) == {  # type: ignore
            "access",
            "refresh",
        }

    def test_with_incorrect_password(self):
        self.client.post(icu.USERS, ici.signup_request(1))
        response = self.client.post(
            icu.AUTHS,
            {**ici.signup_request(1), **ici.DUMMY_PASSWORD},
            QUERY_STRING="action=generate",
        )
        it.assert_equal_responses(response, icr.INCORRECT_PASSWORD)

    def test_with_incorrect_user(self):
        response = self.client.post(
            icu.AUTHS,
            {**ici.signup_request(1)},
            QUERY_STRING="action=generate",
        )
        it.assert_equal_responses(response, icr.USER_NOT_FOUND)
