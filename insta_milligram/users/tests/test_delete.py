import django.test as dt
import django.contrib.auth.models as dcam

import insta_milligram.constants as ic
import insta_milligram.tests as it


class TestView(dt.TestCase):
    def setUp(self):
        self.header = it.signup_and_login(
            self.client,
            ic.inputs.SIGNUP_REQUESTS[0],
        )
        it.signup_and_login(self.client, ic.inputs.SIGNUP_REQUESTS[1])

    def test_correct(self):
        response = self.client.delete(
            ic.urls.USERS_ID_1,
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.SUCCESS)
        assert len(dcam.User.objects.all()) == 1

    def test_incorrect_id(self):
        response = self.client.delete(
            ic.urls.USERS_ID_2,
            headers=self.header,  # type: ignore
        )
        it.assert_equal_responses(response, ic.responses.OPERATION_NOT_ALLOWED)
        assert len(dcam.User.objects.all()) == 2
