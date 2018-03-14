from core.session.model import Session

from tests.session import SessionTestCase
from tests.session import MOCK_SESSION_ID


class TestSessionStore(SessionTestCase):

    def test_default_expiration(self):
        self.assertEqual(1800, self.store.expires, 'Default expiration should be 1800s')

    def test_session_id_generation(self):
        session_id = self.store.generate_session_id()
        self.assertEqual(36, len(session_id), 'Invalid length of session id')

    def test_store_default_none(self):
        self.assertEqual(0, len(self.store), 'Sessions should be empty by default')

    def test_store_add(self):
        self.assertTrue(self.store.add_session(self.session))
        self.assertEqual(1, len(self.store), 'One session should be added')

    def test_store_get(self):
        self.store.add_session(self.session)
        session = self.store.get_internal_session(MOCK_SESSION_ID)
        self.assertIsNotNone(session, 'Session should not be None')

    def test_store_remove(self):
        self.store.add_session(self.session)
        self.assertEqual(1, len(self.store), 'One session should be added')
        self.store.delete_sessions(self.session.session_id)
        self.assertEqual(0, len(self.store), 'Session was not removed')

    def test_store_remove_multiple(self):
        s1 = Session(session_id='1', redis_client=self.redis_client)
        s2 = Session(session_id='2', redis_client=self.redis_client)
        self.assertTrue(self.store.add_session(s1))
        self.assertTrue(self.store.add_session(s2))
        self.assertEqual(2, len(self.store), '2 sessions should be added')
        self.assertEqual(2, self.store.delete_sessions('1', '2'))
        self.assertEqual(0, len(self.store), 'Sessions were not removed')

    def test_remove_sessions_with_pattern(self):
        s1 = Session(session_id='1', redis_client=self.redis_client)
        s2 = Session(session_id='2', redis_client=self.redis_client)
        self.assertTrue(self.store.add_session(s1))
        self.assertTrue(self.store.add_session(s2))
        self.assertEqual(2, len(self.store), '2 sessions should be added')
        self.assertTrue(self.redis_client.set('not_a_session', 5))
        # Delete all sessions
        self.store.delete_redis_session_pattern()
        self.assertEqual(0, len(self.store), 'Sessions were not removed')
        self.assertEqual(5, int(self.redis_client.get('not_a_session')), 'session deletion by default pattern failed')
