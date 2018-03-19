from core.db.models import Answer
from core.db.models import Question
from core.db.models import User

from tests.base import AuthAppTestCase

URI = '/answers/{id}'


class TestWithInvalidParams(AuthAppTestCase):

    def test_with_invalid_id(self):

        # Call
        response = self.fetch(URI.format(id=0), method='DELETE')
        body = self.response_dict(response)

        # Check response
        self.assertEqual(404, response.code)
        self.assertEqual('No Answer with id 0', body['error']['message'])


class TestWithValidParams(AuthAppTestCase):

    def setUp(self):
        super().setUp()
        u1 = User(firstname="Fernando", lastname="Alonso", email="fernando.alonso@mclaren.com")
        q1 = Question(title="What is the fatest car?", body="Which team should I chose to win the F1 world championship?", user=u1)
        self.answer = Answer(body="Message 1", question=q1, user=self.request_user, creator_id=self.request_user.id)
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

    def test_delete(self):

        # Call
        response = self.fetch(URI.format(id=self.answer.id), method='DELETE')

        # Check status code
        self.assertEqual(204, response.code)

        # Check in DB
        alert = self.db.query(Answer).get(self.answer.id)
        self.assertEqual(None, alert)
