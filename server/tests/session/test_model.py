import datetime
import re

from core.session.model import Session

from tests.session import SessionTestCase


class TestSessionModel(SessionTestCase):

    def test_session_hash(self):
        session_hash = self.session.session_hash
        self.assertEqual(20, len(session_hash))

    def test_redis_session_key(self):
        session_key = self.session.redis_session_key
        self.assertTrue(re.search('session:*', session_key))

    def test_is_authenticated(self):
        # With user
        self.session.user_id = 10
        is_authenticated = self.session.is_authenticated
        self.assertTrue(is_authenticated)

        # Without user
        self.session.user_id = None
        is_authenticated = self.session.is_authenticated
        self.assertFalse(is_authenticated)

    def test_redis_representation(self):
        redis_representation = self.session.redis_representation
        self.assertIn('name', redis_representation)
        self.assertIn('mapping', redis_representation)
        self.assertIn('user_id', redis_representation['mapping'])
        self.assertIn('__meta__created_at', redis_representation['mapping'])
        self.assertIn('__meta__last_accessed_at', redis_representation['mapping'])

    def test_to_dict(self):
        result = self.session.to_dict()
        self.assertIn('session_id', result)
        self.assertIn('user_id', result)
        self.assertIn('_created', result)
        self.assertIn('_last_accessed', result)

    def test_from_redis(self):
        redis_representation = self.session.redis_representation
        session_from_redis = Session.from_redis(self.redis_client, redis_representation)
        self.assertEqual(self.session.to_dict(), session_from_redis.to_dict())

    def test_extract_user(self):
        # With user
        self.session.user_id = 10
        redis_representation = self.session.redis_representation
        user_id = Session.extract_user(redis_representation['mapping'])
        self.assertEqual(self.session.user_id, user_id)

        # Without user
        self.session.user_id = None
        redis_representation = self.session.redis_representation
        user_id = Session.extract_user(redis_representation['mapping'])
        self.assertEqual(self.session.user_id, user_id)

    def test_registered_access(self):
        old_date = self.session._last_accessed
        self.session.register_accessed()
        new_date = self.session._last_accessed
        self.assertNotEqual(old_date, new_date)

    def test_save(self):
        # Test invalid session
        self.session._last_accessed = (datetime.datetime.utcnow() - datetime.timedelta(days=1))
        result = self.session.invalidated(30)
        self.assertTrue(result)

        # Test valid session
        self.session._last_accessed = datetime.datetime.utcnow()
        result = self.session.invalidated(30)
        self.assertFalse(result)
