from core.db.models import Answer
from core.db.models import Question
from core.db.models import User

from tests.base import BaseAppTestCase

URI = '/questions/{id}/answers'


class TestWithInvalidParams(BaseAppTestCase):

    def test_with_invalid_id(self):

        # Call
        response = self.fetch(URI.format(id=0), method='DELETE')
        body = self.response_dict(response)

        # Check response
        self.assertEqual(404, response.code)
        self.assertEqual('No Question with id 0', body['error']['message'])


class TestValidParams(BaseAppTestCase):

    def setUp(self):
        super().setUp()
        u1 = User(firstname="Fernando", lastname="Alonso", email="fernando.alonso@mclaren.com")
        self.q1 = Question(title="What is the fatest car?", body="Which team should I chose to win the F1 world championship?", user=u1)
        self.q2 = Question(title="What is the fatest car?", body="Which team should I chose to win the F1 world championship?", user=u1)
        a1 = Answer(body="Message 1", question=self.q1, user=u1)
        a2 = Answer(body="Message 1", question=self.q1, user=u1)
        a3 = Answer(body="Message 1", question=self.q1, user=u1)
        self.db.add(u1)
        self.db.add(self.q1)
        self.db.add(self.q2)
        self.db.add(a1)
        self.db.add(a2)
        self.db.add(a3)
        self.db.commit()

    def tearDown(self):
        self.db.query(Answer).delete()
        self.db.query(Question).delete()
        self.db.query(User).delete()
        self.db.commit()
        super().tearDown()

    def test_list(self):

        # Call
        response = self.fetch(URI.format(id=self.q1.id), method='GET')
        body = self.response_dict(response)

        # Check status code
        self.assertEqual(200, response.code)

        # Check data
        result = body['data']
        self.assertEqual(3, len(result))

    def test_list_empty(self):

        # Call
        response = self.fetch(URI.format(id=self.q2.id), method='GET')
        body = self.response_dict(response)

        # Check status code
        self.assertEqual(200, response.code)

        # Check data
        result = body['data']
        self.assertEqual(0, len(result))
