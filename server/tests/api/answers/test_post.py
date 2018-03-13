import json

from core.db.models import Answer
from core.db.models import Question
from core.db.models import User

from tests.base import BaseAppTestCase

URI = '/questions/{id}/answers'


def get_valid_data():
    return {
        'message': 'Message 1',
    }


class TestWithInvalidParams(BaseAppTestCase):

    def test_with_invalid_id(self):

        # Prepare data
        data = get_valid_data()

        # Call
        response = self.fetch(URI.format(id=0), method='POST', body=json.dumps(data))
        body = self.response_dict(response)

        # Check response
        self.assertEqual(404, response.code)
        self.assertEqual('No Question with id 0', body['error']['message'])


class TestWithValidParams(BaseAppTestCase):

    def setUp(self):
        super().setUp()
        u1 = User(firstname="Fernando", lastname="Alonso", email="fernando.alonso@mclaren.com")
        self.q1 = Question(title="What is the fatest car?", body="Which team should I chose to win the F1 world championship?", user=u1)
        self.db.add(u1)
        self.db.add(self.q1)
        self.db.commit()

    def tearDown(self):
        self.db.query(Answer).delete()
        self.db.query(Question).delete()
        self.db.query(User).delete()
        self.db.commit()
        super().tearDown()

    def test_valid_data(self):

        # Prepare data
        data = get_valid_data()

        # Call
        response = self.fetch(URI.format(id=self.q1.id), method='POST', body=json.dumps(data))
        body = self.response_dict(response)

        # Check status code
        self.assertEqual(201, response.code)

        # Check returned data
        returned_data = body['data']

        keys = ['message']
        for key in keys:
            self.assertIn(key, returned_data)
            self.assertEqual(data[key], returned_data[key])

        # Check existence in db
        answer = self.db.query(Answer).get(returned_data['id'])
        self.assertIsNotNone(answer)

