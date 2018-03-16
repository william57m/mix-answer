from core.db.models import Answer
from core.db.models import Question
from core.db.models import User

from tests.base import AuthAppTestCase

URI = '/questions/{id}'


class TestWithInvalidParams(AuthAppTestCase):

    def test_with_invalid_id(self):

        # Call
        response = self.fetch(URI.format(id=0), method='GET')
        body = self.response_dict(response)

        # Check response
        self.assertEqual(404, response.code)
        self.assertEqual('No Question with id 0', body["error"]['message'])


class TestWithValidParams(AuthAppTestCase):

    def setUp(self):
        super().setUp()
        u1 = User(firstname="Fernando", lastname="Alonso", email="fernando.alonso@mclaren.com")
        self.q1 = Question(title="What is the fatest car?", body="Which team should I chose to win the F1 world championship?", user=u1, creator_id=self.request_user.id)
        a1 = Answer(message="Message 1", question=self.q1, user=self.request_user, creator_id=self.request_user.id)
        self.db.add(u1)
        self.db.add(self.q1)
        self.db.add(a1)
        self.db.commit()

    def tearDown(self):
        self.db.query(Answer).delete()
        self.db.query(Question).delete()
        self.db.query(User).delete()
        self.db.commit()
        super().tearDown()

    def test_get(self):

        # Call
        response = self.fetch(URI.format(id=self.q1.id), method='GET')
        body = self.response_dict(response)

        # Check status code
        self.assertEqual(200, response.code)

        # Check question
        question = body['question']
        self.assertIn('title', question)
        self.assertEqual('What is the fatest car?', question['title'])
        self.assertIn('body', question)
        self.assertEqual('Which team should I chose to win the F1 world championship?', question['body'])

        # Check answer
        answers = body['answers']
        self.assertEqual(1, len(answers))
