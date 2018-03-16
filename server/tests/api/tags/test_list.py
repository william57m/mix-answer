from core.db.models import Tag

from tests.base import BaseAppTestCase

URI = '/tags'


class TestWithValidParams(BaseAppTestCase):

    def setUp(self):
        super().setUp()
        t1 = Tag(label="Python")
        t2 = Tag(label="JavaScript")
        self.db.add(t1)
        self.db.add(t2)
        self.db.commit()

    def tearDown(self):
        self.db.query(Tag).delete()
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
        self.assertEqual(2, len(result))
