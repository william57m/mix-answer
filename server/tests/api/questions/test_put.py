import json

from core.db.models import Question
from core.db.models import User

from tests.base import AuthAppTestCase

URI = '/questions/{id}'


def get_valid_data():
    return {
        'title': 'Title',
        'body': 'Body'
    }


class TestWithInvalidParams(AuthAppTestCase):

    def test_with_invalid_id(self):

        # Call
        response = self.fetch(URI.format(id=0), method='PUT', body=json.dumps(dict()))
        body = self.response_dict(response)

        # Check response
        self.assertEqual(404, response.code)
        self.assertEqual('No Question with id 0', body["error"]['message'])


class TestWithValidParams(AuthAppTestCase):

    def setUp(self):
        super().setUp()
        u1 = User(firstname="Fernando", lastname="Alonso", email="fernando.alonso@mclaren.com")
        self.q1 = Question(title="What is the fatest car?", body="Which team should I chose to win the F1 world championship?", user=u1, creator_id=self.request_user.id)
        self.db.add(u1)
        self.db.add(self.q1)
        self.db.commit()

    def tearDown(self):
        self.db.query(Question).delete()
        self.db.query(User).delete()
        self.db.commit()
        super().tearDown()

    def test_valid_data(self):

        # Prepare data
        data = get_valid_data()

        # Call
        response = self.fetch(URI.format(id=self.q1.id), method='PUT', body=json.dumps(data))
        body = self.response_dict(response)

        # Check status code
        self.assertEqual(200, response.code)

        # Check returned data
        returned_data = body['data']
        self.assertIn('title', returned_data)
        self.assertEqual(data['title'], returned_data['title'])
        self.assertIn('body', returned_data)
        self.assertEqual(data['body'], returned_data['body'])
