import json

from core.db.models import Question
from core.db.models import User

from tests.base import BaseAppTestCase

URI = '/questions/{id}'


def get_valid_data():
    return {
        'title': 'Title',
        'body': 'Body'
    }


class TestInvalidParamsQuestion(BaseAppTestCase):
    """ Test update with invalid parameters """

    def test_with_invalid_id(self):
        """ Test with invalid alert id """

        # Call
        response = self.fetch(URI.format(id=0), method='PUT', body=json.dumps(dict()))
        body = self.response_dict(response)

        # Check response
        self.assertEqual(404, response.code)
        self.assertEqual('No Question with id 0', body["error"]['message'])


class TestUpdateQuestion(BaseAppTestCase):
    """ Test update valid parameters """

    def setUp(self):
        super().setUp()
        u1 = User(firstname="Fernando", lastname="Alonso", email="fernando.alonso@mclaren.com")
        self.q1 = Question(title="What is the fatest car?", body="Which team should I chose to win the F1 world championship?", user=u1)
        self.db.add(u1)
        self.db.add(self.q1)
        self.db.commit()

    def tearDown(self):
        self.db.query(Question).delete()
        self.db.query(User).delete()
        self.db.commit()
        super().tearDown()

    def test_update_all(self):
        """ Test update all data """

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
