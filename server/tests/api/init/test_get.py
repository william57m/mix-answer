from tests.base import AuthAppTestCase

URI = '/init'


class TestValidParams(AuthAppTestCase):

    def test_with_user(self):

        # Call
        response = self.fetch(URI, method='GET')
        body = self.response_dict(response)

        # Check status code
        self.assertEqual(200, response.code)

        # Check data
        self.assertIn('user', body)

    def test_without_user(self):

        # Call
        response = self.fetch(URI, method='GET', headers={})
        body = self.response_dict(response)

        # Check status code
        self.assertEqual(200, response.code)

        # Check data
        self.assertNotIn('user', body)
