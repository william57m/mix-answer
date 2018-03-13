from core.db.models import Answer
from core.db.models import Question
from core.db.models import User
from core.db.models import Vote

from tests.base import BaseAppTestCase

URI = '/answers/{id}/votes'


class TestWithInvalidParams(BaseAppTestCase):

    def test_with_invalid_id(self):

        # Call
        response = self.fetch(URI.format(id=0), method='POST', body='{}')
        body = self.response_dict(response)

        # Check response
        self.assertEqual(404, response.code)
        self.assertEqual('No Answer with id 0', body['error']['message'])


class TestWithValidParams(BaseAppTestCase):

    def setUp(self):
        super().setUp()
        self.u1 = User(id=1, firstname="Fernando", lastname="Alonso", email="fernando.alonso@mclaren.com")
        q1 = Question(title="What is the fatest car?", body="Which team should I chose to win the F1 world championship?", user=self.u1)
        self.a1 = Answer(message="Message 1", question=q1)
        self.a2 = Answer(message="Message 1", question=q1)
        self.db.add(self.u1)
        self.db.add(q1)
        self.db.add(self.a1)
        self.db.add(self.a2)
        self.db.commit()
        v = Vote(user_id=self.u1.id, answer_id=self.a2.id)
        self.db.add(v)
        self.db.commit()

    def tearDown(self):
        self.db.query(Vote).delete()
        self.db.query(Answer).delete()
        self.db.query(Question).delete()
        self.db.query(User).delete()
        self.db.commit()
        super().tearDown()

    def test_vote(self):

        # Call
        response = self.fetch(URI.format(id=self.a1.id), method='POST', body='{}')

        # Check status code
        self.assertEqual(201, response.code)

        # Check in DB
        vote = self.db.query(Vote).filter(Vote.user_id == self.u1.id) \
                                  .filter(Vote.answer_id == self.a1.id) \
                                  .first()
        self.assertNotEqual(None, vote)

    def test_unvote(self):

        # Call
        response = self.fetch(URI.format(id=self.a2.id), method='POST', body='{}')

        # Check status code
        self.assertEqual(201, response.code)

        # Check in DB
        vote = self.db.query(Vote).filter(Vote.user_id == self.u1.id) \
                                  .filter(Vote.answer_id == self.a2.id) \
                                  .first()
        self.assertEqual(None, vote)
