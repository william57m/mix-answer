from unittest import TestCase

from core.services.redis import RedisClient
from core.session.model import Session
from core.session.store import SessionStore

from tests.base import config

MOCK_SESSION_ID = 'df1c472b-125b-48ab-b3c7-9484fb9b2e6e'


class SessionTestCase(TestCase):

    def setUp(self):
        super().setUp()
        self.redis_client = RedisClient.from_config(config)
        self.redis_client.flushdb()
        self.store = SessionStore(redis_client=self.redis_client)
        self.session = Session(session_id=MOCK_SESSION_ID, redis_client=self.redis_client)

    def tearDown(self):
        self.redis_client.flushdb()
