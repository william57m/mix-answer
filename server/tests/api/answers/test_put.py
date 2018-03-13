import json

from core.db.models import Answer
from core.db.models import Question
from core.db.models import User

from tests.base import BaseAppTestCase

URI = '/answers/{id}'


def get_valid_data():
    return {
        'message': 'New Message'
    }


class TestWithInvalidParams(BaseAppTestCase):

    def test_with_invalid_id(self):

        # Call
        response = self.fetch(URI.format(id=0), method='PUT', body=json.dumps(dict()))
        body = self.response_dict(response)

        # Check response
        self.assertEqual(404, response.code)
        self.assertEqual('No Answer with id 0', body["error"]['message'])


class TestWithValidParams(BaseAppTestCase):

    def setUp(self):
        super().setUp()
        u1 = User(firstname="Fernando", lastname="Alonso", email="fernando.alonso@mclaren.com")
        q1 = Question(title="What is the fatest car?", body="Which team should I chose to win the F1 world championship?", user=u1)
        self.answer = Answer(message="Message 1", question=q1)
        self.db.add(u1)
        self.db.add(q1)
        self.db.add(self.answer)
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
        response = self.fetch(URI.format(id=self.answer.id), method='PUT', body=json.dumps(data))
        body = self.response_dict(response)

        # Check status code
        self.assertEqual(200, response.code)

        # Check returned data
        returned_data = body['data']
        self.assertIn('message', returned_data)
        self.assertEqual(data['message'], returned_data['message'])
