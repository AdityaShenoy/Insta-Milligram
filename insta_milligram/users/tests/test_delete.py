import django.test as dt
import django.contrib.auth.models as dam

import insta_milligram.constants as c
import insta_milligram.tests as t


class TestView(dt.TestCase):
    def setUp(self):
        self.header = t.signup_and_login(
            self.client,
            c.inputs.SIGNUP_REQUESTS[0],
        )
        t.signup_and_login(self.client, c.inputs.SIGNUP_REQUESTS[1])

    def test_correct(self):
        response = self.client.delete(
            c.urls.USERS_ID_1,
            headers=self.header,  # type: ignore
        )
        t.assert_equal_responses(response, c.responses.SUCCESS)
        assert len(dam.User.objects.all()) == 1

    def test_incorrect_id(self):
        response = self.client.delete(
            c.urls.USERS_ID_2,
            headers=self.header,  # type: ignore
        )
        t.assert_equal_responses(response, c.responses.OPERATION_NOT_ALLOWED)
        assert len(dam.User.objects.all()) == 2
