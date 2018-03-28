from core.db.models import Answer
from core.db.models import Question
from core.db.models import User

from tests.base import BaseAppTestCase

URI = '/questions'


class TestWithValidParams(BaseAppTestCase):

    def setUp(self):
        super().setUp()
        u1 = User(firstname="Fernando", lastname="Alonso", email="fernando.alonso@mclaren.com")
        q1 = Question(title="What is the fatest car?", body="Which team should I chose to win the F1 world championship?", user=u1)
        q2 = Question(title="What is the fatest car?", body="Which team should I chose to win the F1 world championship?", user=u1)
        q3 = Question(title="What is the fatest car?", body="Which team should I chose to win the F1 world championship?", user=u1)
        q4 = Question(title="What is the fatest car?", body="Which team should I chose to win the F1 world championship?", user=u1)
        a1 = Answer(body="Message 1", question=q1, user=u1)
        self.db.add(u1)
        self.db.add(q1)
        self.db.add(q2)
        self.db.add(q3)
        self.db.add(q4)
        self.db.add(a1)
        self.db.commit()

    def tearDown(self):
        self.db.query(Answer).delete()
        self.db.query(Question).delete()
        self.db.query(User).delete()
        self.db.commit()
        super().tearDown()

    def test_list(self):

        # Call
        response = self.fetch(URI, method='GET')
        body = self.response_dict(response)

        # Check status code
        self.assertEqual(200, response.code)

        # Check data
        result = body['data']
        self.assertEqual(4, len(result))


    def test_unanswered_list(self):

        # Call
        response = self.fetch(URI + '?unanswered=true', method='GET')
        body = self.response_dict(response)

        # Check status code
        self.assertEqual(200, response.code)

        # Check data
        result = body['data']
        self.assertEqual(3, len(result))
