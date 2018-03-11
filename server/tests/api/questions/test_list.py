import json

from core.db.models import Question
from core.db.models import User

from tests.base import BaseAppTestCase

URI = '/questions'


class TestListQuestion(BaseAppTestCase):

    def setUp(self):
        super().setUp()
        u1 = User(firstname="Fernando", lastname="Alonso", email="fernando.alonso@mclaren.com")
        q1 = Question(title="What is the fatest car?", body="Which team should I chose to win the F1 world championship?", user=u1)
        q2 = Question(title="What is the fatest car?", body="Which team should I chose to win the F1 world championship?", user=u1)
        self.db.add(u1)
        self.db.add(q1)
        self.db.add(q2)
        self.db.commit()

    def tearDown(self):
        self.db.query(Question).delete()
        self.db.query(User).delete()
        self.db.commit()
        super().tearDown()

    def test_list(self):
        """ Test get all companies """

        # Call
        response = self.fetch(URI, method='GET')
        body = self.response_dict(response)

        # Check status code
        self.assertEqual(200, response.code)

        # Check data
        result = body['data']
        self.assertEqual(2, len(result))
