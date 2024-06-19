import rest_framework.test as rt  # type: ignore

import insta_milligram.constants.responses as icr
import insta_milligram.tests as it


def test_without_login(method: str, url: str):
    response = rt.APIClient().__getattribute__(method)(url)
    it.assert_equal_responses(response, icr.TOKEN_MISSING)
