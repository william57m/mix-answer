import json

from core.db.models import Question
from core.db.models import User

from tests.base import BaseAppTestCase

URI = '/questions'


def get_valid_data():
    return {
        'title': 'Title',
        'body': 'Body'
    }


class TestWithMissingParams(BaseAppTestCase):

    def tearDown(self):
        """ Teardown test """

        self.db.query(Question).delete()
        self.db.commit()
        super().tearDown()

    def test_missing_title(self):
        """ Test create with missing title """

        # Prepare data
        data = get_valid_data()
        data.pop('title')

        # Call
        response = self.fetch(URI, method='POST', body=json.dumps(data))
        body = self.response_dict(response)

        # Check response
        self.assertEqual(400, response.code)
        self.assertEqual('Param title is missing', body["error"]['message'])

    def test_missing_body(self):

        # Prepare data
        data = get_valid_data()
        data.pop('body')

        # Call
        response = self.fetch(URI, method='POST', body=json.dumps(data))
        body = self.response_dict(response)

        # Check response
        self.assertEqual(400, response.code)
        self.assertEqual('Param body is missing', body["error"]['message'])


class TestWithValidParams(BaseAppTestCase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        self.db.query(Question).delete()
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

        keys = ['title', 'body']
        for key in keys:
            self.assertIn(key, returned_data)
            self.assertEqual(data[key], returned_data[key])

        # Check existence in db
        question = self.db.query(Question).get(returned_data['id'])
        self.assertIsNotNone(question)
