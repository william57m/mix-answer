import json

from core.db.models import Answer
from core.db.models import Question
from core.db.models import User
from core.db.models import VoteAnswer

from tests.base import AuthAppTestCase

URI = '/answers/{id}/votes'


def get_valid_data():
    return {
        'up_down': True
    }


class TestWithInvalidParams(AuthAppTestCase):

    def setUp(self):
        super().setUp()
        self.u1 = User(firstname="Fernando", lastname="Alonso", email="fernando.alonso@mclaren.com")
        self.q1 = Question(title="What is the fatest car?", body="Which team should I chose to win the F1 world championship?", user=self.u1)
        self.a1 = Answer(body="Message 1", question=self.q1, user=self.u1)
        self.db.add(self.u1)
        self.db.add(self.q1)
        self.db.add(self.a1)
        self.db.commit()

    def tearDown(self):
        self.db.query(VoteAnswer).delete()
        self.db.query(Answer).delete()
        self.db.query(Question).delete()
        self.db.query(User).delete()
        self.db.commit()
        super().tearDown()

    def test_with_invalid_id(self):

        # Prepare data
        data = get_valid_data()

        # Call
        response = self.fetch(URI.format(id=0), method='POST', body=json.dumps(data))
        body = self.response_dict(response)

        # Check response
        self.assertEqual(404, response.code)
        self.assertEqual('No Answer with id 0', body['error']['message'])

    def test_with_invalid_up_down(self):

        # Prepare data
        data = get_valid_data()
        data['up_down'] = 'blabla'

        # Call
        response = self.fetch(URI.format(id=self.a1.id), method='POST', body=json.dumps(data))
        body = self.response_dict(response)

        # Check response
        self.assertEqual(400, response.code)
        self.assertEqual('Param up_down must be a boolean', body['error']['message'])


class TestWithMissingParams(AuthAppTestCase):

    def setUp(self):
        super().setUp()
        self.u1 = User(firstname="Fernando", lastname="Alonso", email="fernando.alonso@mclaren.com")
        self.q1 = Question(title="What is the fatest car?", body="Which team should I chose to win the F1 world championship?", user=self.u1)
        self.a1 = Answer(body="Message 1", question=self.q1, user=self.u1)
        self.db.add(self.u1)
        self.db.add(self.q1)
        self.db.add(self.a1)
        self.db.commit()

    def tearDown(self):
        self.db.query(VoteAnswer).delete()
        self.db.query(Answer).delete()
        self.db.query(Question).delete()
        self.db.query(User).delete()
        self.db.commit()
        super().tearDown()

    def test_missing_up_down(self):

        # Prepare data
        data = get_valid_data()
        data.pop('up_down')

        # Call
        response = self.fetch(URI.format(id=self.a1.id), method='POST', body=json.dumps(data))
        body = self.response_dict(response)

        # Check response
        self.assertEqual(400, response.code)
        self.assertEqual('Param up_down is missing', body['error']['message'])


class TestWithValidParams(AuthAppTestCase):

    def setUp(self):
        super().setUp()
        self.u1 = User(firstname="Fernando", lastname="Alonso", email="fernando.alonso@mclaren.com")
        self.q1 = Question(title="What is the fatest car?", body="Which team should I chose to win the F1 world championship?", user=self.u1)
        self.a1 = Answer(body="Message 1", question=self.q1, user=self.u1)
        self.a2 = Answer(body="Message 1", question=self.q1, user=self.u1)
        self.a3 = Answer(body="Message 1", question=self.q1, user=self.u1, vote_counter=1)
        self.db.add(self.u1)
        self.db.add(self.q1)
        self.db.add(self.a1)
        self.db.add(self.a2)
        self.db.commit()
        v = VoteAnswer(user_id=self.request_user.id, answer_id=self.a3.id)
        self.db.add(v)
        self.db.commit()

    def tearDown(self):
        self.db.query(VoteAnswer).delete()
        self.db.query(Answer).delete()
        self.db.query(Question).delete()
        self.db.query(User).delete()
        self.db.commit()
        super().tearDown()

    def test_vote_up(self):

        # Prepare data
        data = get_valid_data()
        data['up_down'] = True

        # Call
        response = self.fetch(URI.format(id=self.a1.id), method='POST', body=json.dumps(data))

        # Check status code
        self.assertEqual(200, response.code)

        # Check vote in DB
        vote = self.db.query(VoteAnswer).filter(VoteAnswer.user_id == self.request_user.id) \
                                        .filter(VoteAnswer.answer_id == self.a1.id) \
                                        .first()
        self.assertNotEqual(None, vote)
        self.assertEqual(data['up_down'], vote.up_down)

        # Check counter in DB
        answer = self.db.query(Answer).get(self.a1.id)
        self.assertEqual(1, answer.vote_counter)

    def test_vote_down(self):

        # Prepare data
        data = get_valid_data()
        data['up_down'] = False

        # Call
        response = self.fetch(URI.format(id=self.a2.id), method='POST', body=json.dumps(data))

        # Check status code
        self.assertEqual(200, response.code)

        # Check vote in DB
        vote = self.db.query(VoteAnswer).filter(VoteAnswer.user_id == self.request_user.id) \
                                        .filter(VoteAnswer.answer_id == self.a2.id) \
                                        .first()
        self.assertNotEqual(None, vote)
        self.assertEqual(data['up_down'], vote.up_down)

        # Check counter in DB
        answer = self.db.query(Answer).get(self.a2.id)
        self.assertEqual(-1, answer.vote_counter)

    def test_unvote(self):

        # Prepare data
        data = get_valid_data()

        # Call
        response = self.fetch(URI.format(id=self.a3.id), method='POST', body=json.dumps(data))

        # Check status code
        self.assertEqual(200, response.code)

        # Check vote in DB
        vote = self.db.query(VoteAnswer).filter(VoteAnswer.user_id == self.request_user.id) \
                                        .filter(VoteAnswer.answer_id == self.a3.id) \
                                        .first()
        self.assertEqual(None, vote)

        # Check counter in DB
        answer = self.db.query(Answer).get(self.a3.id)
        self.assertEqual(0, answer.vote_counter)
