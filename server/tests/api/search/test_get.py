from urllib.parse import quote

from core.db.models import Answer
from core.db.models import Question
from core.db.models import User

from tests.base import BaseAppTestCase

URI = '/search?q={search}'


class TestValidParams(BaseAppTestCase):

    def setUp(self):
        super().setUp()

        # User
        u1 = User(firstname="Fernando", lastname="Alonso", email="fernando.alonso@mclaren.com")
        self.db.add(u1)

        # Questions
        questions = [
            {"title": "What is an apple?", "body": "This is the first body?", "user": u1},
            {"title": "What is an orange?", "body": "This is the second body", "user": u1},
            {"title": "What is an ananas?", "body": "This is the third body", "user": u1},
            {"title": "What is a mango?", "body": "This is the fourth body", "user": u1},
            {"title": "How taste a banana?", "body": "This is the fifth body", "user": u1}
        ]
        self.questions = []
        for question in questions:
            q = Question(**question)
            self.db.add(q)
            self.questions.append(q)

        # Answer
        answers = [
            {"body": "Message 1", "question": self.questions[0], "user": u1},
            {"body": "Message 1", "question": self.questions[0], "user": u1},
            {"body": "Message 1", "question": self.questions[1], "user": u1},
            {"body": "Message 1", "question": self.questions[2], "user": u1}
        ]
        self.answers = []
        for answer in self.answers:
            a = Answer(**answer)
            self.db.add(a)
            self.answers.append(a)

        self.db.commit()

    def tearDown(self):
        self.db.query(Answer).delete()
        self.db.query(Question).delete()
        self.db.query(User).delete()
        self.db.commit()
        super().tearDown()

    def _search(self, text):
        response = self.fetch(URI.format(search=quote(text)), method='GET')
        body = self.response_dict(response)

        # Check data
        self.assertEqual(200, response.code)
        return body['data']

    def test_search_1(self):
        result = self._search('apple')
        self.assertEqual(1, len(result))

    def test_search_2(self):
        result = self._search('apple first body')
        self.assertEqual(1, len(result))

    def test_search_3(self):
        result = self._search('this fourth body')
        self.assertEqual(1, len(result))

    def test_search_4(self):
        result = self._search('second or third or fifth body')
        self.assertEqual(3, len(result))

    def test_search_5(self):
        result = self._search('apple or orange or mango')
        self.assertEqual(3, len(result))

    def test_search_6(self):
        result = self._search('body -first')
        self.assertEqual(4, len(result))
