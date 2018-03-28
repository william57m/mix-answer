import json

from core.db.models import User

from tests.base import BaseAppTestCase

URI = '/users'


def get_valid_data():
    return {
        'firstname': 'Kimi',
        'lastname': 'Raikkonen',
        'email': 'kimi.raikkonen@ferrari.it',
        'password': 'FeRRaRi'
    }


class TestWithMissingParams(BaseAppTestCase):

    def test_missing_firstname(self):
        """ Test create with missing firstname """

        # Prepare data
        data = get_valid_data()
        data.pop('firstname')

        # Call
        response = self.fetch(URI, method='POST', body=json.dumps(data))
        body = self.response_dict(response)

        # Check response
        self.assertEqual(400, response.code)
        self.assertEqual('Param firstname is missing', body["error"]['message'])

    def test_missing_lastname(self):
        """ Test create with missing lastname """

        # Prepare data
        data = get_valid_data()
        data.pop('lastname')

        # Call
        response = self.fetch(URI, method='POST', body=json.dumps(data))
        body = self.response_dict(response)

        # Check response
        self.assertEqual(400, response.code)
        self.assertEqual('Param lastname is missing', body["error"]['message'])

    def test_missing_email(self):
        """ Test create with missing email """

        # Prepare data
        data = get_valid_data()
        data.pop('email')

        # Call
        response = self.fetch(URI, method='POST', body=json.dumps(data))
        body = self.response_dict(response)

        # Check response
        self.assertEqual(400, response.code)
        self.assertEqual('Param email is missing', body["error"]['message'])

    def test_missing_password(self):
        """ Test create with missing password """

        # Prepare data
        data = get_valid_data()
        data.pop('password')

        # Call
        response = self.fetch(URI, method='POST', body=json.dumps(data))
        body = self.response_dict(response)

        # Check response
        self.assertEqual(400, response.code)
        self.assertEqual('Param password is missing', body["error"]['message'])


class TestWithValidParams(BaseAppTestCase):

    def tearDown(self):
        self.db.query(User).delete()
        self.db.commit()
        super().tearDown()

    def test_valid_data(self):

        # Prepare data
        data = get_valid_data()

        # Call
        response = self.fetch(URI, method='POST', body=json.dumps(data))
        body = self.response_dict(response)

        # Check status code
        self.assertEqual(201, response.code)

        # Check returned data
        returned_data = body['data']

        keys = ['firstname', 'lastname', 'email']
        for key in keys:
            self.assertIn(key, returned_data)
            self.assertEqual(data[key], returned_data[key])

        # Check existence in db
        user = self.db.query(User).get(returned_data['id'])
        self.assertIsNotNone(user)
